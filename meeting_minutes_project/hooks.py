# -*- coding: utf-8 -*-
# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    This hook is executed before the module installation.
    1. It cleans up orphan foreign key references in related models to prevent
       constraint errors during the installation of the new model structure.
    2. It renames the old tables to preserve the data for the post-init migration.
    """
    _logger.info("Starting pre-init hook for meeting_minutes data migration.")

    # --- DATA CLEANUP STEP ---
    tables_to_clean = {
        'mail_activity': 'meeting_minutes_id',
        'meeting_minutes_discuss_point': 'meeting_minutes_id',
    }

    _logger.info("Cleaning up orphan references in related tables...")
    for table, column in tables_to_clean.items():
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s", (table,)
        )
        if not cr.fetchone():
            _logger.warning(f"Table '{table}' not found, skipping cleanup for it.")
            continue

        cr.execute(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = %s AND column_name = %s",
            (table, column)
        )
        if cr.fetchone():
            query = f"""
                UPDATE {table}
                SET {column} = NULL
                WHERE {column} IS NOT NULL
                AND {column} NOT IN (SELECT id FROM meeting_minutes_mixin);
            """
            cr.execute(query)
            _logger.info(f"Cleaned up orphan references in '{table}.{column}'.")
        else:
            _logger.warning(
                f"Column '{column}' not found in table '{table}', skipping cleanup."
            )

    _logger.info("Cleanup of orphan references finished.")

    # --- RENAME TABLES STEP ---
    _logger.info("Starting to rename old tables for backup.")
    tables_to_rename = [
        ('meeting_minutes', 'old_meeting_minutes'),
        ('meeting_minutes_discuss_point', 'old_meeting_minutes_discuss_point'),
        ('meeting_minutes_signature', 'old_meeting_minutes_signature'),
        ('means_communication', 'old_means_communication'),
        ('meeting_minutes_res_partner_rel', 'old_meeting_minutes_res_partner_rel'),
    ]

    for old_name, new_name in tables_to_rename:
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s", (old_name,)
        )
        if cr.fetchone():
            _logger.info(f"Rename the table '{old_name}' to '{new_name}'.")
            cr.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
        else:
            _logger.warning(f"'{old_name}' : table not found.")

    _logger.info("END Pre INIT HOOK")


def post_init_hook(cr, registry):
    """
    This hook is executed after the module installation.
    It migrates data from the old, backed-up tables to the new ones,
    and replicates the onchange logic for data consistency.
    """
    _logger.info("Starting post-init hook for meeting_minutes data migration.")
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Step 1: Migrate 'means_communication' to 'meeting.channel'
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

    # Step 2: Migrate main records and apply business logic
    old_to_new_id_map = {}
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_meeting_minutes'"
    )
    if cr.fetchone():
        cr.execute("SELECT * FROM old_meeting_minutes")
        old_minutes_data = cr.dictfetchall()
        _logger.info(
            f"{len(old_minutes_data)} records to migrate from 'old_meeting_minutes'."
        )

        project_minute_fields = env['meeting.minutes.project']._fields

        for row in old_minutes_data:
            old_id = row['id']
            start_date, end_date = row.get('start_date'), row.get('end_date')

            if not start_date:
                _logger.warning(
                    f"Skipping old record id={old_id} due to missing start_date."
                )
                continue
            if end_date and start_date > end_date:
                _logger.warning(f"Swapping inverted dates for old record id={old_id}.")
                start_date, end_date = end_date, start_date
            elif not end_date:
                end_date = start_date

            vals = {
                'task_id': row.get('task_id'),
                'start_date': start_date,
                'end_date': end_date,
                'meeting_channel_id': channel_map.get(
                    row.get('mean_communication_id')
                ),
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
                    f"Failed to create record for old_id={old_id}. Error: {e}"
                )
                continue
        _logger.info("Main records migration completed.")

    # --- Step 3: Migrate 'discuss_point_ids' (CORRECTED) ---
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_meeting_minutes_discuss_point'"
    )
    if cr.fetchone():
        cr.execute(
            "SELECT meeting_minutes_id, sequence, task_id, notes "
            "FROM old_meeting_minutes_discuss_point"
        )
        for row in cr.dictfetchall():
            new_meeting_id = old_to_new_id_map.get(row['meeting_minutes_id'])
            if new_meeting_id:
                env['meeting.minutes.discuss.point'].create({
                    'meeting_minutes_id': new_meeting_id,
                    'sequence': row.get('sequence'),
                    'task_id': row.get('task_id'),
                    'notes': row.get('notes'),
                })
        _logger.info("Migration of 'discuss_point_ids' completed.")

    # --- Step 4: Update 'homework_ids' ---
    for old_id, new_id in old_to_new_id_map.items():
        cr.execute(
            "UPDATE mail_activity SET meeting_minutes_id = %s "
            "WHERE meeting_minutes_id = %s", (new_id, old_id)
        )
    _logger.info("Update of 'homework_ids' in 'mail.activity' completed.")

    # --- Step 5: Migrate 'signature_ids' (CORRECTED) ---
    cr.execute(
        "SELECT 1 FROM information_schema.tables "
        "WHERE table_name = 'old_meeting_minutes_signature'"
    )
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
    for table_name in tables_to_drop:
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            (table_name,)
        )
        if cr.fetchone():
            _logger.info(f"Dropping old table '{table_name}'.")
            cr.execute(f"DROP TABLE {table_name} CASCADE")

    # Step 7: Recreate empty tables for clean uninstallation
    _logger.info(
        "Recreating empty tables to allow clean uninstallation of old modules."
    )
    tables_to_recreate = [
        "means_communication",
        "meeting_minutes",
        "meeting_minutes_discuss_point",
        "meeting_minutes_signature",
        "meeting_minutes_res_partner_rel",
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