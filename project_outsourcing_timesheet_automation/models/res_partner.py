# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    subcontracting_auto_time_entries = fields.Boolean(
        "Subcontracting - Automate Time Entries"
    )
    employee_id = fields.Many2one('hr.employee', "Employee for Time Entries")
