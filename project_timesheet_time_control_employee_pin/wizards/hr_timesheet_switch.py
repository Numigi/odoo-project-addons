# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class HrTimesheetSwitch(models.TransientModel):
    _inherit = "hr.timesheet.switch"

    running_timer_id = fields.Many2one(
        comodel_name="account.analytic.line",
        string="Previous timer",
        ondelete="cascade",
        readonly=True,
        default=None,
        help="This timer is running and will be stopped",
    )

    @api.onchange('pin')
    def _onchange_pin(self):
        self.employee_id = self.env['hr.employee'].search(
                [('pin', '=', self.pin)], limit=1).id if self.pin else False
        self.running_timer_id = \
            self._default_running_timer_id(self.employee_id)
