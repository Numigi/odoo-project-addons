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

    @api.multi
    def write(self, vals):
        if vals.get('task_id'):
            vals['origin_task_id'] = vals['task_id']
        return super().write(vals)
