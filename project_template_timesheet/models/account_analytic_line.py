# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.constrains('task_id')
    def _check_template_task_can_not_have_timesheets(self):
        lines_with_template_task = self.filtered(
            lambda l: l.task_id.is_template)
        if lines_with_template_task:
            line = lines_with_template_task[0]
            raise ValidationError(_(
                "The timesheet line {line} could not be added to the task {task} "
                "because this task is a template."
            ).format(line=line.display_name, task=line.task_id.display_name))
