# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError


class Task(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        if "project_id" in vals:
            project = self.env["project.project"].browse(vals["project_id"])
            tasks_with_different_project = self.filtered(
                lambda t: t.project_id != project
            )

            for task in tasks_with_different_project:
                task._check_has_no_timesheet()
                task._check_has_no_subtask_timesheet()

        return super().write(vals)

    def _check_has_no_timesheet(self):
        if self.sudo().timesheet_ids:
            raise ValidationError(
                _(
                    "Timesheets have already been entered on this task ({task}). "
                    "In order to modify the project of this task, you may "
                    "close the task and create another in the target project."
                ).format(task=self.display_name)
            )

    def _check_has_no_subtask_timesheet(self):
        timesheets = (
            self.env["account.analytic.line"]
            .sudo()
            .search([("task_id.parent_id", "=", self.id)])
        )

        if timesheets:
            raise ValidationError(
                _(
                    "Timesheets have already been entered on a sub-task ({subtask}). "
                    "In order to modify the project of the parent task ({task}), there must "
                    "be no time on the parent task, nor on its child tasks."
                ).format(
                    task=self.display_name,
                    subtask=timesheets[0].task_id.display_name
                )
            )
