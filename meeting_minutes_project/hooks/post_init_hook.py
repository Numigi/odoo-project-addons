# -*- coding: utf-8 -*-
# © 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):

    _logger.info(" START POST INIT HOOK")
    env = api.Environment(cr, SUPERUSER_ID, {})

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
            "Migration Done : means_communication ")

    old_to_new_id_map = {}
    cr.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes'")
    if cr.fetchone():
        cr.execute("""
            SELECT id, task_id, start_date, end_date, mean_communication_id,
                   planned_point, additional_note, resources, risks,
                   certificate_enabled, certificate_report_id
            FROM old_meeting_minutes
        """)
        old_minutes_data = cr.dictfetchall()
        _logger.info(
            f"{len(old_minutes_data)} records to migrate from 'old_meeting_minutes'.")

        for row in old_minutes_data:
            old_id = row['id']
            vals = {'task_id': row['task_id'], 'start_date': row['start_date'],
                'end_date': row['end_date'],
                'meeting_channel_id': channel_map.get(row['mean_communication_id']),
                'planned_points': row['planned_point'],
                'discussed_points': row['additional_note'],
                'resources': row['resources'], 'risks': row['risks'],
                'certificate_enabled': row.get('certificate_enabled', False),
                'certificate_report_id': row.get('certificate_report_id'), }
            new_minute = env['meeting.minutes.project'].create(vals)
            old_to_new_id_map[old_id] = new_minute.id

            # Attendees Migration
            cr.execute("""
                SELECT res_partner_id FROM old_meeting_minutes_res_partner_rel WHERE meeting_minutes_id = %s
            """, (old_id,))
            partner_ids = [r[0] for r in cr.fetchall()]
            if partner_ids:
                new_minute.write({'partner_ids': [(6, 0, partner_ids)]})

        _logger.info(
            "Migration Done  : from meeting.minutes to  'meeting.minutes.project' ")

    cr.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes_discuss_point'")
    if cr.fetchone():
        cr.execute(
            "SELECT meeting_minutes_id, sequence, task_id, notes FROM old_meeting_minutes_discuss_point")
        for row in cr.dictfetchall():
            new_meeting_id = old_to_new_id_map.get(row['meeting_minutes_id'])
            if new_meeting_id:
                env['meeting.minutes.discuss.point'].create(
                    {'meeting_minutes_id': new_meeting_id, 'sequence': row['sequence'],
                        'task_id': row['task_id'], 'notes': row['notes'], })
        _logger.info("Migration Done : Discuss point")

    for old_id, new_id in old_to_new_id_map.items():
        cr.execute("""
            UPDATE mail_activity 
            SET res_id = %s, res_model = 'meeting.minutes.project' 
            WHERE res_id = %s AND res_model = 'meeting.minutes'
        """, (new_id, old_id))
        cr.execute("""
            UPDATE mail_activity
            SET meeting_minutes_id = %s
            WHERE meeting_minutes_id = %s
        """, (new_id, old_id))
    _logger.info("UPDATE homeworks in  'mail.activity' Done ")

    cr.execute(
        "SELECT 1 FROM information_schema.tables WHERE table_name = 'old_meeting_minutes_signature'")
    if cr.fetchone():
        cr.execute("""
            SELECT minutes_id, partner_id, type_, state, signature_datetime, signature, access_token
            FROM old_meeting_minutes_signature
        """)
        for row in cr.dictfetchall():
            new_meeting_id = old_to_new_id_map.get(row['minutes_id'])
            if new_meeting_id:
                env['meeting.minutes.signature'].create(
                    {'minutes_id': new_meeting_id, 'partner_id': row['partner_id'],
                        'type_': row['type_'], 'state': row['state'],
                        'signature_datetime': row['signature_datetime'],
                        'signature': row['signature'],
                        'access_token': row['access_token'], })
        _logger.info("Migration Done : certificate signature.")


    tables_to_drop = ['old_meeting_minutes', 'old_meeting_minutes_discuss_point',
        'old_meeting_minutes_signature', 'old_means_communication',
        'old_meeting_minutes_res_partner_rel', ]
    for table_name in tables_to_drop:
        cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = %s",
            (table_name,))
        if cr.fetchone():
            _logger.info(f"Delete old table'{table_name}'.")
            cr.execute(f"DROP TABLE {table_name}")


    _logger.info("END :  POST INIT HOOK")