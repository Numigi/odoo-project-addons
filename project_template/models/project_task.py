# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.osv.expression import AND

SHOW_TASK_TEMPLATES = 'show_task_templates'


def should_apply_default_template_filter(domain, context):
    template_field_in_domain = any(
        isinstance(el, (list, tuple)) and el[0] == 'is_template'
        for el in domain
    )
    return not (template_field_in_domain or context.get(SHOW_TASK_TEMPLATES))


class ProjectTask(models.Model):

    _inherit = 'project.task'

    is_template = fields.Boolean()

    @api.model
    def _get_values_for_invisible_template_fields(self):
        return {
            'date_start': False,
            'date_end': False,
            'date_deadline': False,
            'email_cc': False,
            'email_from': False,
            'kanban_state': 'normal',
            'partner_id': False,
            'stage_id': False,
            'user_id': False,
        }

    @api.multi
    def write(self, vals):
        if vals.get('is_template'):
            vals = dict(vals, **self._get_values_for_invisible_template_fields())

        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get('is_template'):
            vals = dict(vals, **self._get_values_for_invisible_template_fields())

        return super().create(vals)

    @api.model
    def _search(self, args, *args_, **kwargs):
        """Hide templates from searches by default."""
        if should_apply_default_template_filter(args, self._context):
            args = AND((args or [], [('is_template', '=', False)]))
        return super()._search(args, *args_, **kwargs)


class ProjectTaskTemplatePropagationToSubtask(models.Model):
    """Integrate is_template with the concept of subtasks.

    Suppose a task is defined with subtasks.

    If we set the task as a template, then all its subtasks will becomme
    templates as well.
    """

    _inherit = 'project.task'

    child_ids = fields.One2many(context={
        'active_test': False,
        SHOW_TASK_TEMPLATES: True,
    })

    def action_subtask(self):
        """Display child templates when clicking on the subtask smart button."""
        res = super().action_subtask()
        res['context'][SHOW_TASK_TEMPLATES] = True
        return res

    @api.onchange('parent_id')
    def _onchange_parent_set_is_template(self):
        if self.parent_id:
            self.is_template = self.parent_id.is_template

    def _update_is_template_from_parent_task(self):
        subtasks = self.filtered(lambda t: t.parent_id)
        for subtask in subtasks:
            if subtask.is_template != subtask.parent_id.is_template:
                subtask.is_template = subtask.parent_id.is_template

    @api.multi
    def write(self, vals):
        res = super().write(vals)

        if 'is_template' in vals:
            child_tasks = self.mapped('child_ids')
            if child_tasks:
                child_tasks.write({'is_template': vals['is_template']})

        if vals.get('parent_id'):
            self._update_is_template_from_parent_task()

        return res

    @api.model
    def create(self, vals):
        task = super().create(vals)
        task._update_is_template_from_parent_task()
        return task
