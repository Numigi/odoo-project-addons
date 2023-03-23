# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ProjectTaskTemplateAdd(models.TransientModel):

    _name = 'project.task.template.add'
    _description = 'Task Template Selection Wizard'

    project_id = fields.Many2one('project.project')
    task_template_ids = fields.Many2many(
        'project.task',
        'project_task_template_add_rel',
        'wizard_id',
        'task_id',
    )

    def _check_only_task_template_selected(self):
        normal_tasks = self.task_template_ids.filtered(
            lambda t: not t.is_template)
        if normal_tasks:
            raise ValidationError(_(
                'The selected task {} is not a template.'
            ).format(normal_tasks[0].display_name))

    def _copy_task_template(self, task):
        return task.copy({
            'project_id': self.project_id.id,
            'name': task.name,  # prevent `(copy)` in task name
            'stage_id': False,
            'parent_id': False,
        })

    def validate(self):
        self._check_only_task_template_selected()

        for task in self.task_template_ids:
            new_template = self._copy_task_template(task)

            for subtask in task.child_ids:
                new_subtask_template = self._copy_task_template(subtask)
                new_subtask_template.parent_id = new_template

        return True
