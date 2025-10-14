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

    # --- DATA CLEANUP STEP (Based on your correct analysis) ---
    # Tables that have a foreign key to the old 'meeting_minutes' model.
    # We set the FK to NULL if it points to a non-existent record.
    tables_to_clean = {
        'mail_activity': 'meeting_minutes_id',
        'meeting_minutes_discuss_point': 'meeting_minutes_id',
    }

    _logger.info("Cleaning up orphan references in related tables...")
    for table, column in tables_to_clean.items():
        # Check if the table and column exist before attempting to clean
        cr.execute("""
            SELECT 1 FROM information_schema.tables WHERE table_name = %s
        """, (table,))
        if not cr.fetchone():
            _logger.warning(f"Table '{table}' not found, skipping cleanup for it.")
            continue

        cr.execute("""
            SELECT 1 FROM information_schema.columns WHERE table_name = %s AND column_name = %s
        """, (table, column))
        if cr.fetchone():
            # This query nullifies references to meeting.minutes records that no longer exist.
            # It uses 'meeting_minutes_mixin' as the source of truth for valid IDs, which is correct
            # because the new 'meeting.minutes.project' inherits from it.
            query = f"""
                UPDATE {table}
                SET {column} = NULL
                WHERE {column} IS NOT NULL
                AND {column} NOT IN (SELECT id FROM meeting_minutes_mixin);
            """
            cr.execute(query)
            _logger.info(f"Cleaned up orphan references in '{table}.{column}'.")
        else:
            _logger.warning(f"Column '{column}' not found in table '{table}', skipping cleanup.")

    _logger.info("Cleanup of orphan references finished.")
    # --- END OF CLEANUP STEP ---

    _logger.info("Starting to rename old tables for backup.")

    # Tables to rename
    tables_to_rename = [
        ('meeting_minutes', 'old_meeting_minutes'),
        ('meeting_minutes_discuss_point', 'old_meeting_minutes_discuss_point'),
        ('meeting_minutes_signature', 'old_meeting_minutes_signature'),
        ('means_communication', 'old_means_communication'),
        ('meeting_minutes_res_partner_rel', 'old_meeting_minutes_res_partner_rel'),
    ]

    for old_name, new_name in tables_to_rename:
        cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = %s", (old_name,))
        if cr.fetchone():
            _logger.info(f"Renommage de la table '{old_name}' en '{new_name}'.")
            cr.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
        else:
            _logger.warning(f"La table '{old_name}' n'a pas été trouvée, renommage ignoré.")

    _logger.info("END  Pre INIT HOOK")



def post_init_hook(cr, registry):
        """
        This hook is executed after the module installation.
        It migrates data from the old, backed-up tables to the new ones.
        """
        _logger.info("Starting post-init hook for meeting_minutes data migration.")
        env = api.Environment(cr, SUPERUSER_ID, {})

        # --- Step 1: Migrate 'means_communication' to 'meeting.channel' ---
        channel_map = {}
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = 'old_means_communication'")
        if cr.fetchone():
            cr.execute("SELECT id, name FROM old_means_communication")
            for row in cr.dictfetchall():
                channel = env['meeting.channel'].search([('name', '=', row['name'])],
                    limit=1)
                if not channel:
                    channel = env['meeting.channel'].create({'name': row['name']})
                channel_map[row['id']] = channel.id
            _logger.info(
                "Migration from 'means_communication' to 'meeting.channel' completed.")

        # --- Step 2: Migrate 'meeting_minutes' to 'meeting.minutes.project' ---
        old_to_new_id_map = {}
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes'")
        if cr.fetchone():
            cr.execute("SELECT * FROM old_meeting_minutes")
            old_minutes_data = cr.dictfetchall()
            _logger.info(
                f"{len(old_minutes_data)} records to migrate from 'old_meeting_minutes'.")

            project_minute_fields = env['meeting.minutes.project']._fields

            for row in old_minutes_data:
                old_id = row['id']

                # --- ROBUST DATE HANDLING (with your swapping logic) ---
                start_date = row.get('start_date')
                end_date = row.get('end_date')

                if not start_date:
                    _logger.warning(
                        f"Skipping old meeting minute with id={old_id} due to missing start_date.")
                    continue

                if end_date and start_date > end_date:
                    _logger.warning(
                        f"Swapping inverted dates for old meeting minute with id={old_id}.")
                    start_date, end_date = end_date, start_date  # Inversion des dates
                elif not end_date:
                    _logger.warning(
                        f"Setting missing end_date for old meeting minute with id={old_id}.")
                    end_date = start_date
                # --- END OF DATE HANDLING ---

                vals = {'task_id': row.get('task_id'), 'start_date': start_date,
                    'end_date': end_date, 'meeting_channel_id': channel_map.get(
                        row.get('mean_communication_id')),
                    'planned_points': row.get('planned_point'),
                    'discussed_points': row.get('additional_note'),
                    'resources': row.get('resources'), 'risks': row.get('risks'), }

                if 'certificate_enabled' in project_minute_fields and 'certificate_enabled' in row:
                    vals['certificate_enabled'] = row['certificate_enabled']
                if 'certificate_report_id' in project_minute_fields and 'certificate_report_id' in row:
                    vals['certificate_report_id'] = row['certificate_report_id']

                try:
                    new_minute = env['meeting.minutes.project'].create(vals)
                    old_to_new_id_map[old_id] = new_minute.id

                    cr.execute("""
                        SELECT res_partner_id FROM old_meeting_minutes_res_partner_rel WHERE meeting_minutes_id = %s
                    """, (old_id,))
                    partner_ids = [r[0] for r in cr.fetchall()]
                    if partner_ids:
                        new_minute.write({'partner_ids': [(6, 0, partner_ids)]})
                except Exception as e:
                    _logger.error(
                        f"Failed to create new meeting minute for old_id={old_id}. Error: {e}")
                    continue

            _logger.info(
                "Migration from 'meeting.minutes' to 'meeting.minutes.project' completed.")



        _logger.info("Post-init hook completed successfully.")