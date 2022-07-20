# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    subcontracting_auto_time_entries = fields.Boolean(
        "Subcontracting - Automate Time Entries",
        company_dependent=True,
    )
    employee_id = fields.Many2one(
        'hr.employee', "Employee for Time Entries",
        company_dependent=True,
    )

    @api.model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + \
            ['subcontracting_auto_time_entries', 'employee_id']

    @api.onchange('subcontracting_auto_time_entries')
    def _onchange_subcontracting_auto_time_entries(self):
        for record in self:
            if not record.subcontracting_auto_time_entries:
                record.employee_id = False
