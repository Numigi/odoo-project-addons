# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from .project_task import SHOW_TASK_TEMPLATES


class Project(models.Model):

    _inherit = 'project.project'

    is_template = fields.Boolean()
    template_task_ids = fields.One2many('project.task', compute="_compute_template_task_ids")

    @api.model
    def _create_task_from_template(self, template):
        return template.copy({
            'project_id': template.project_id.id,
            'name': template.name,  # prevent `(copy)` in task name
            'is_template': False,
            'parent_id': False,
            'origin_template_id': template.id,
        })

    @api.model
    def _convert_template_to_task(self, template):
        task = template.effective_task_ids

        if not task:
            task = self._create_task_from_template(template)

        child_templates_with_no_task = template.child_ids.filtered(
            lambda c: not c.effective_task_ids)

        for child_template in child_templates_with_no_task:
            subtask = self._create_task_from_template(child_template)
            subtask.parent_id = task

    @api.multi
    def convert_templates_to_tasks(self):
        """Convert template tasks to tasks.

        This method is idempotent. It may be called multiple times on
        the same project.

        If a task template was already converted, it will not be converted
        a second time.

        If a subtask template was not converted, it will be converted
        even if the parent template was converted before.
        """
        all_tasks = self.with_context(**{SHOW_TASK_TEMPLATES: True}).mapped('task_ids')
        templates = all_tasks.filtered(lambda t: t.is_template)
        parent_templates = templates.filtered(lambda t: not t.parent_id)

        for template in parent_templates:
            self._convert_template_to_task(template)

        return True

    def _compute_template_task_ids(self):
        for rec in self:
            rec.template_task_ids = rec.env["project.task"].search([
                ("project_id", "=", rec.id),
                ("is_template", "=", True),
            ])

class ProjectWithTemplateTaskCount(models.Model):

    _inherit = 'project.project'

    task_template_count = fields.Integer(compute='_compute_task_template_count')

    def _compute_task_template_count(self):
        domain = [('project_id', 'in', self.ids), ('is_template', '=', True)]
        task_data = (
            self.env['project.task'].with_context(**{SHOW_TASK_TEMPLATES: True})
            .read_group(domain, ['project_id'], ['project_id'])
        )
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.task_template_count = result.get(project.id, 0)
