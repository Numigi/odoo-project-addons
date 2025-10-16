# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, SUPERUSER_ID, fields

_logger = logging.getLogger(__name__)


def migrate_channels(env, cr):
    """Step 1: Migrate 'means_communication' to 'meeting.channel'"""
    channel_map = {}
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_means_communication'"
    )
    if cr.fetchone():
        cr.execute("SELECT id, name FROM old_means_communication")
        for row in cr.dictfetchall():
            channel = env['meeting.channel'].search(
                [('name', '=', row['name'])], limit=1
            )
            if not channel:
                channel = env['meeting.channel'].create({'name': row['name']})
            channel_map[row['id']] = channel.id
        _logger.info(
            "Migration from 'means_communication' to 'meeting.channel' completed."
        )
    return channel_map


def migrate_meeting_minutes(env, cr, channel_map):
    """Step 2: Migrate main meeting_minutes.project records"""
    old_to_new_id_map = {}
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_meeting_minutes'"
    )
    if not cr.fetchone():
        return old_to_new_id_map

    cr.execute("SELECT * FROM old_meeting_minutes")
    old_minutes_data = cr.dictfetchall()
    _logger.info("%d records to migrate from 'old_meeting_minutes'.", len(old_minutes_data))

    project_minute_fields = env['meeting.minutes.project']._fields

    for row in old_minutes_data:
        old_id = row['id']
        start_date, end_date = row.get('start_date'), row.get('end_date')
        if not start_date:
            _logger.warning(
                "Missing start date: Set to False - old id=%s", old_id
            )
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
            _logger.error(
                "Failed to create record for old_id=%s. Error: %s", old_id, e
            )
            continue

    _logger.info("Main records migration completed.")
    return old_to_new_id_map


def migrate_discuss_points(env, cr, old_to_new_id_map):
    """Step 3: Migrate 'discuss_point_ids' with generic fallback"""
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_meeting_minutes_discuss_point'"
    )
    if not cr.fetchone():
        return

    generic_meeting = env['meeting.minutes.project'].search(
        [('name', '=', 'Generic Discuss Points')], limit=1
    )
    if not generic_meeting:
        generic_meeting = env['meeting.minutes.project'].create({
            'name': 'Generic Discuss Points',
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today(),
            'planned_points': 'Auto-generated for discuss points with NULL meeting_id',
        })
    generic_meeting_id = generic_meeting.id

    cr.execute(
        "SELECT meeting_minutes_id, sequence, task_id, notes "
        "FROM old_meeting_minutes_discuss_point"
    )
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

    _logger.info(
        "Migration of 'discuss_point_ids' completed. Total: %d, Linked: %d, "
        "Generic fallback: %d", count_total, count_linked, count_generic)


def update_homework_activities(env, cr, old_to_new_id_map):
    """Step 4: Update 'homework_ids' in mail.activity"""
    _logger.info("Updating homework_ids for migrated meetings...")
    cr.execute(
        "SELECT activity_id, old_meeting_minutes_id FROM temp_activity_migration_map;")

    updates = []
    for activity_id, old_meeting_id in cr.fetchall():
        new_meeting_id = old_to_new_id_map.get(old_meeting_id)
        if new_meeting_id:
            updates.append(f"({activity_id}, {new_meeting_id})")

    if updates:
        # Construit une seule grosse requête UPDATE
        query = """
                    UPDATE mail_activity AS ma
                    SET meeting_minutes_id = data.new_meeting_id
                    FROM (VALUES {updates_str}) AS data(activity_id, new_meeting_id)
                    WHERE ma.id = data.activity_id;
                """.format(updates_str=",".join(updates))

        cr.execute(query)
        _logger.info(f"Restored {len(updates)} homework links.")


def migrate_signatures(env, cr, old_to_new_id_map):
    """Step 5: Migrate 'signature_ids'"""
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_meeting_minutes_signature'"
    )
    if not cr.fetchone():
        return

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


def recreate_empty_tables(cr):
    """Step 6: Final cleanup / recreate minimal tables for clean uninstall"""
    _logger.info("Starting final cleanup of old tables.")
    tables_to_recreate = ["meeting_minutes"]
    for table_name in tables_to_recreate:
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            (table_name,)
        )
        if not cr.fetchone():
            _logger.info("Recreating empty table: %s", table_name)
            cr.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY);")


def post_init_hook(cr, registry):
    """Main post-init hook"""
    _logger.info("Starting post-init hook for meeting_minutes data migration.")
    env = api.Environment(cr, SUPERUSER_ID, {})

    channel_map = migrate_channels(env, cr)
    old_to_new_id_map = migrate_meeting_minutes(env, cr, channel_map)
    migrate_discuss_points(env, cr, old_to_new_id_map)
    update_homework_activities(env, cr, old_to_new_id_map)
    migrate_signatures(env, cr, old_to_new_id_map)
    recreate_empty_tables(cr)

    _logger.info("Post-init hook completed successfully.")
