# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.constrains("project_id")
    def _check_project_move_allow_timesheet(self):
        """Check if a line is moved to another project,
        the target project must allow timesheet"""

        error_message = _(
            "You cannot move a task linked to a timesheet line in a project if its "
            "stage does not allow it. (Task: {}, Project: {}, Project Stage: {})"
        )

        for rec in self:
            project = rec.project_id
            timesheets = rec.timesheet_ids

            if timesheets and project and not project.allow_timesheets:
                stage = project.stage_id
                message = error_message.format(
                    rec.display_name, project.display_name, stage.display_name
                )
                raise ValidationError(message)
