# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _should_apply_constraints(self, env):
        def _is_testing():
            return getattr(threading.current_thread(), "testing", False)
        return not _is_testing() or env.context.get(
            "enable_project_stage_allow_timesheet_constraint"
        )

    @api.constrains("task_id")
    def _check_task_project_allow_timesheet(self):
        if not self._should_apply_constraints(self.env):
            return

        error_message = _(
            "You can't link a time sheet line to a task if its project's stage"
            " does not allow it. (Task: {}, Project: {}, Project Stage: {})"
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
