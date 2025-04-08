# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        """
        Propagate the value of the project to the subtask when it
        is changed on the parent task.
        """
        res = super().write(vals)
        for task in self:
            if task.child_ids and "project_id" in vals:
                task.child_ids.write(
                    {
                        "project_id": vals["project_id"],
                        "display_project_id": vals["project_id"],
                    }
                )
        return res

    @api.constrains("project_id", "parent_id", "display_project_id")
    def _check_subtask_project_consistency(self):
        for task in self:
            if task.parent_id and task.project_id != task.parent_id.project_id:
                raise ValidationError(
                    _(
                        "The subtask '{subtask}' must be in the same project "
                        "as its parent task '{parent_task}'."
                    ).format(
                        subtask=task.display_name,
                        parent_task=task.parent_id.display_name,
                    )
                )
