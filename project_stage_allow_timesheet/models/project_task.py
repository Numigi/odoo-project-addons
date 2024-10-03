
# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _should_apply_constraints(self, env):
        def _is_testing():
            return getattr(threading.current_thread(), "testing", False)
        return not _is_testing() or env.context.get(
            "enable_project_stage_allow_timesheet_constraint"
        )

    @api.constrains("project_id")
    def _check_project_move_allow_timesheet(self):
        """ Check if a line is moved to another project,
        the target project must allow time sheet """
        if not self._should_apply_constraints(self.env):
            return

        error_message = _(
            "You cannot move a task linked to a timesheet line in a project if its"
            "stage does not allow it. (Task: {}, Project: {}, Project Stage: {})"
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
