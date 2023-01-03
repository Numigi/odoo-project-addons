# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import UserError


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

    def action_switch(self):
        """Stop old timer, start new one."""
        self.ensure_one()
        _fields = self.env["account.analytic.line"]._fields.keys()
        self.read(_fields)
        values = self._convert_to_write(self._cache)
        # check if user selected a valid employee PIN
        if values.get('pin'):
            employee = self.env['hr.employee'].search(
                [('pin', '=', values.get('pin'))], limit=1)
            values['employee_id'] = employee.id if employee else False
            if not employee or not employee.user_id:
                raise UserError(_(
                    "Please choose an existing employee PIN and ensure that "
                    "the selected employee is related to an existing user."))
        # Stop old timer
        self.with_context(
            resuming_lines=self.ids,
            stop_dt=self.date_time,
        ).running_timer_id.button_end_work()

        # Start new timer
        new = self.env["account.analytic.line"].create({
            field: value for (field, value) in values.items()
            if field in _fields
        })
        # Display created timer record if requested
        if self.env.context.get("show_created_timer"):
            form_view = self.env.ref("hr_timesheet.hr_timesheet_line_form")
            return {
                "res_id": new.id,
                "res_model": new._name,
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "view_type": "form",
                "views": [
                    (form_view.id, "form"),
                ],
            }
        # Close wizard and reload view
        return {
            "type": "ir.actions.act_multi",
            "actions": [
                {"type": "ir.actions.act_window_close"},
                {"type": "ir.actions.act_view_reload"},
            ],
        }

    @api.onchange('pin')
    def _onchange_pin(self):
        self.employee_id = self.env['hr.employee'].search(
                [('pin', '=', self.pin)], limit=1).id if self.pin else False
        self.running_timer_id = \
            self._default_running_timer_id(self.employee_id)
