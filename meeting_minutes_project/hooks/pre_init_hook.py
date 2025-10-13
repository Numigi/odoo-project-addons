# -*- coding: utf-8 -*-
# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)

def pre_init_hook(cr):

    _logger.info("Start PRE INIT HOOK")

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