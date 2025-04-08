# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.constrains("task_id", "project_id")
    def _check_task_project_allow_timesheets(self):
        error_message = _(
            "You can't link a timesheet line to a task if its project's stage"
            " does not allow it. (Task: {}, Project: {}, Project Stage: {})"
        )
        for rec in self:
            project = rec.project_id
            stage = project.stage_id
            if project and stage and not stage.allow_timesheets:
                message = error_message.format(
                    rec.display_name, project.display_name, stage.display_name
                )
                raise ValidationError(message)
