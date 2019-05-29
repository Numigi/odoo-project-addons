# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class TimesheetLine(models.Model):
    """Set the origin task of timesheet lines.

    The origin task is copied from the field task_id when filled.
    task_id is only filled when the analytic line is a timesheet line.
    """

    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        if vals.get('task_id'):
            vals['origin_task_id'] = vals['task_id']
        return super().create(vals)

    def _propagate_origin_task_to_timesheet_lines(self):
        """Backward propagation of origin_task_id to task_id.

        This allows the system to behave in a more transparent way
        when manually changing the value of origin_task_id
        for a timesheet line.
        """
        lines_to_update = self.filtered(
            lambda l: l.task_id and l.origin_task_id != l.task_id
        )
        for line in lines_to_update:
            line.task_id = line.origin_task_id

    @api.multi
    def write(self, vals):
        if vals.get('task_id'):
            vals['origin_task_id'] = vals['task_id']

        super().write(vals)

        if vals.get('origin_task_id'):
            self._propagate_origin_task_to_timesheet_lines()

        return True
