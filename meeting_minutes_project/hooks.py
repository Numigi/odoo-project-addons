# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    Pre-init hook executed before the module installation.
    1. Cleans up orphan foreign key references in related tables to prevent
       constraint errors during module installation.
    2. Renames old tables to preserve data for post-init migration.
    """
    _logger.info("Starting pre-init hook for meeting_minutes data migration.")

    # --- STEP 0 : Mail activity Backup ---
    _logger.info("Backing up mail.activity to meeting_minutes relationship...")

    cr.execute("DROP TABLE IF EXISTS temp_activity_migration_map;")
    cr.execute("""
                CREATE TABLE temp_activity_migration_map (
                    activity_id INTEGER,
                    old_meeting_minutes_id INTEGER
                );
            """)
    # Populate the temporary table
    cr.execute("""
                INSERT INTO temp_activity_migration_map
                 (activity_id, old_meeting_minutes_id)
                SELECT id, meeting_minutes_id
                FROM mail_activity
                WHERE meeting_minutes_id IS NOT NULL;
            """)
    _logger.info(f"Backed up {cr.rowcount} mail.activity relations.")
    # Nullify the column to avoid FK constraint errors during installation
    cr.execute("UPDATE mail_activity SET meeting_minutes_id = NULL;")
    _logger.info("Set mail_activity.meeting_minutes_id to NULL.")

    # --- STEP 1: Data Cleanup ---
    _logger.info("Cleaning up orphan references in related tables...")
    tables_to_clean = {
        'mail_activity': 'meeting_minutes_id',
        'meeting_minutes_discuss_point': 'meeting_minutes_id',
    }

    for table, column in tables_to_clean.items():
        cr.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = %s", (table,)
        )
        if not cr.fetchone():
            _logger.warning(f"Table '{table}' not found, skipping cleanup.")
            continue

        cr.execute(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = %s AND column_name = %s",
            (table, column),
        )
        if not cr.fetchone():
            _logger.warning(
                f"Column '{column}' not found in table '{table}', skipping cleanup."
            )
            continue

        if table == 'meeting_minutes_discuss_point':
            # Orphan discuss points will be reassigned later in post-init
            _logger.info(f"Orphan discuss points in '{table}' will be reassigned post-init.")
        else:
            query = f"""
                UPDATE {table}
                SET {column} = NULL
                WHERE {column} IS NOT NULL
                AND {column} NOT IN (SELECT id FROM meeting_minutes_mixin);
            """
            cr.execute(query)
            _logger.info(f"Cleaned up orphan references in '{table}.{column}'.")

    _logger.info("Cleanup of orphan references finished.")

    # --- STEP 2: Rename old tables ---
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
            _logger.info(f"Renaming table '{old_name}' to '{new_name}'.")
            cr.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
        else:
            _logger.warning(f"Table '{old_name}' not found, skipping rename.")

    _logger.info("END Pre INIT HOOK")
