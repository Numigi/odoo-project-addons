# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, _
from odoo.exceptions import ValidationError


class ProjectTaskSubtaskSameProject(models.Model):
    _inherit = 'project.task'

    def _check_subtask_not_in_different_project(self):
        subtasks = self.filtered(lambda t: t.parent_id)

        for subtask in subtasks:
            task = subtask.parent_id
            if subtask.project_id != task.project_id:
                raise ValidationError(_(
                    'The task {task} is in the project {task_project}. '
                    'The subtask {subtask} must be in the same project.'
                ).format(
                    task=task.display_name,
                    task_project=task.project_id.display_name,
                    subtask=subtask.display_name,
                ))

    def write(self, vals):
        """ Propagate the value of the project to the subtask when it is changed on the parent task."""
        res = super().write(vals)
        for task in self:
            if task.child_ids and 'project_id' in vals:
                task.child_ids.write({'project_id': vals['project_id']})
            task._check_subtask_not_in_different_project()
        return res

    def action_subtask(self):
        """Remove project filters from the subtask action context."""
        res = super().action_subtask()

        context_vars_to_remove = (
            'search_default_project_id',
        )

        res['context'] = {
            k: v for k, v in res['context'].items() if
            k not in context_vars_to_remove
        }
        return res
