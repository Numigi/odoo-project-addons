# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.constrains('task_id')
    def _check_task_project_allow_timesheet(self):
        error_message = _(
            "You can't link a time sheet line to a task if its project's stage does not allow it. "
            "(Task: {}, Project: {}, Project Stage: {})"
        )
        for rec in self:
            task = rec.task_id
            project = rec.project_id
            stage = project.stage_id
            if task and project and stage and not stage.allow_timesheet:
                message = error_message.format(
                    rec.display_name, project.display_name, stage.display_name
                )
                raise ValidationError(message)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.constrains('project_id')
    def _check_project_move_allow_timesheet(self):
        """ Check if a line is moved to another project, the target project must allow time sheet """
        error_message = _(
            "You cannot move a task linked to a timesheet line in a project if its stage does not allow it. "
            "(Task: {}, Project: {}, Project Stage: {})"
        )

        for rec in self:
            project = rec.project_id
            time_sheets = rec.timesheet_ids

            if time_sheets and project and not project.allow_timesheets:
                stage = project.stage_id
                message = error_message.format(
                    rec.display_name, project.display_name, stage.display_name
                )
                raise ValidationError(message)
