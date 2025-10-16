# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, SUPERUSER_ID, fields

_logger = logging.getLogger(__name__)

def post_init_hook(cr, registry):
    """
    Post-init hook executed after module installation.
    Migrates old data and assigns orphan discuss points to a generic meeting.
    """
    _logger.info("Starting post-init hook for meeting_minutes data migration.")
    env = api.Environment(cr, SUPERUSER_ID, {})

    # --- Step 1: Migrate 'means_communication' to 'meeting.channel' ---
    channel_map = {}
    cr.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'old_means_communication'"
    )
    if cr.fetchone():
        cr.execute("SELECT id, name FROM old_means_communication")
        for row in cr.dictfetchall():
            channel = env['meeting.channel'].search([('name', '=', row['name'])], limit=1)
            if not channel:
                channel = env['meeting.channel'].create({'name': row['name']})
            channel_map[row['id']] = channel.id
        _logger.info("Migration from 'means_communication' to 'meeting.channel' completed.")

    # --- Step 2: Migrate main meeting_minutes.project records ---
    old_to_new_id_map = {}
    cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes'")
    if cr.fetchone():
        cr.execute("SELECT * FROM old_meeting_minutes")
        old_minutes_data = cr.dictfetchall()
        _logger.info(f"{len(old_minutes_data)} records to migrate from 'old_meeting_minutes'.")

        project_minute_fields = env['meeting.minutes.project']._fields

        for row in old_minutes_data:
            old_id = row['id']
            start_date, end_date = row.get('start_date'), row.get('end_date')
            if not start_date:
                _logger.warning(f"Missing start date:Set to False - old id={old_id} ")
                start_date = False
            if end_date and start_date > end_date:
                start_date, end_date = end_date, start_date
            elif not end_date:
                end_date = start_date

            vals = {
                'task_id': row.get('task_id'),
                'start_date': start_date,
                'end_date': end_date,
                'meeting_channel_id': channel_map.get(row.get('mean_communication_id')),
                'planned_points': row.get('planned_point'),
                'discussed_points': row.get('additional_note'),
                'resources': row.get('resources'),
                'risks': row.get('risks'),
            }
            if 'certificate_enabled' in project_minute_fields:
                vals['certificate_enabled'] = row.get('certificate_enabled', False)
            if 'certificate_report_id' in project_minute_fields:
                vals['certificate_report_id'] = row.get('certificate_report_id')

            try:
                new_minute = env['meeting.minutes.project'].create(vals)
                old_to_new_id_map[old_id] = new_minute.id

                if new_minute.task_id:
                    task = new_minute.task_id
                    new_minute._set_document_ref(task, 'project.task')
                    new_minute._set_meeting_minutes_name(task)
                    new_minute._set_attendees(task)
                    new_minute.project_id = task.project_id.id

                cr.execute(
                    "SELECT res_partner_id FROM old_meeting_minutes_res_partner_rel "
                    "WHERE meeting_minutes_id = %s", (old_id,)
                )
                partner_ids = [r[0] for r in cr.fetchall()]
                if partner_ids:
                    new_minute.partner_ids = [(6, 0, partner_ids)]

            except Exception as e:
                _logger.error(f"Failed to create record for old_id={old_id}. Error: {e}")
                continue
        _logger.info("Main records migration completed.")

    # --- Step 3: Migrate 'discuss_point_ids' with generic fallback ---
    cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes_discuss_point'")
    if cr.fetchone():
        # Create or fetch generic meeting for orphan discuss points
        generic_meeting = env['meeting.minutes.project'].search(
            [('name', '=', 'Generic Discuss Points')], limit=1)
        if not generic_meeting:
            generic_meeting = env['meeting.minutes.project'].create({
                'name': 'Generic Discuss Points',
                'start_date': fields.Date.today(),
                'end_date': fields.Date.today(),
                'planned_points': 'Auto-generated for discuss points with NULL meeting_id',
            })
        generic_meeting_id = generic_meeting.id

        cr.execute("SELECT meeting_minutes_id, sequence, task_id, notes FROM old_meeting_minutes_discuss_point")
        count_total = count_generic = count_linked = 0

        for row in cr.dictfetchall():
            count_total += 1
            old_meeting_id = row['meeting_minutes_id']
            if old_meeting_id:
                new_meeting_id = old_to_new_id_map.get(old_meeting_id, generic_meeting_id)
                if new_meeting_id == generic_meeting_id:
                    count_generic += 1
                else:
                    count_linked += 1
            else:
                new_meeting_id = generic_meeting_id
                count_generic += 1

            env['meeting.minutes.discuss.point'].create({
                'meeting_minutes_id': new_meeting_id,
                'sequence': row.get('sequence'),
                'task_id': row.get('task_id'),
                'notes': row.get('notes'),
            })

        _logger.info(f"Migration of 'discuss_point_ids' completed. Total: {count_total}, Linked: {count_linked}, Generic fallback: {count_generic}")

    # --- Step 4: Update 'homework_ids' in mail.activity ---
    _logger.info("Updating homework_ids for migrated meetings...")

    homework_activity = env.ref("project_task_meeting_minutes.activity_homework")

    activities = env["mail.activity"].search(
        [("activity_type_id", "=", homework_activity.id),
            ("res_model", "=", "project.task")])
    _logger.info("Found %d homework activities" % len(activities))

    for act in activities:
        meeting = env['meeting.minutes.project'].search([('task_id', '=', act.res_id)],
            limit=1)
        if meeting:
            act.write({'meeting_minutes_id': meeting.id})
            _logger.info("activity for %s "% meeting.id )

    # --- Step 5: Migrate 'signature_ids' ---
    cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes_signature'")
    if cr.fetchone():
        cr.execute("SELECT * FROM old_meeting_minutes_signature")
        for row in cr.dictfetchall():
            new_meeting_id = old_to_new_id_map.get(row['minutes_id'])
            if new_meeting_id:
                env['meeting.minutes.signature'].create({
                    'minutes_id': new_meeting_id,
                    'partner_id': row.get('partner_id'),
                    'type_': row.get('type_'),
                    'state': row.get('state'),
                    'signature_datetime': row.get('signature_datetime'),
                    'signature': row.get('signature'),
                    'access_token': row.get('access_token'),
                })
        _logger.info("Migration of 'signature_ids' completed.")

    # Step 6: Final Cleanup
    _logger.info("Starting final cleanup of old tables.")
    tables_to_drop = [
        'old_meeting_minutes_discuss_point',
        'old_meeting_minutes_signature',
        'old_meeting_minutes_res_partner_rel',
        'old_meeting_minutes',
        'old_means_communication',
    ]
    # for table_name in tables_to_drop:
    #     cr.execute(
    #         "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
    #         (table_name,)
    #     )
    #     if cr.fetchone():
    #         _logger.info(f"Dropping old table '{table_name}'.")
    #         cr.execute(f"DROP TABLE {table_name} CASCADE")

    # Step 7: Recreate empty tables for clean uninstallation
    # _logger.info(
    #     "Recreating empty tables to allow clean uninstallation of old modules."
    #)
    tables_to_recreate = [
    #     "means_communication",
          "meeting_minutes",
    #     "meeting_minutes_discuss_point",
    #     "meeting_minutes_signature",
    #     "meeting_minutes_res_partner_rel",
     ]
    for table_name in tables_to_recreate:
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            (table_name,)
        )
        if not cr.fetchone():
            _logger.info(f"Recreating empty table: {table_name}")
            cr.execute(
                f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY);"
            )
    _logger.info("Post-init hook completed successfully.")