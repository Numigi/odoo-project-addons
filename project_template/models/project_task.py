# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.osv.expression import AND

SHOW_TASK_TEMPLATES = "show_task_templates"


def should_apply_default_template_filter(domain, context):
    template_field_in_domain = any(
        isinstance(el, (list, tuple)) and el[0] == "is_template" for el in domain
    )
    return not (template_field_in_domain or context.get(SHOW_TASK_TEMPLATES))


class ProjectTask(models.Model):

    _inherit = "project.task"

    is_template = fields.Boolean()

    @api.multi
    def write(self, vals):
        if vals.get("is_template"):
            vals = dict(vals, **self._get_values_for_invisible_template_fields())

        super().write(vals)

        for template in self.filtered("is_template"):
            template._empty_invisible_template_fields()

        return True

    @api.model
    def create(self, vals):
        if vals.get("is_template"):
            vals = dict(vals, **self._get_values_for_invisible_template_fields())

        return super().create(vals)

    def _empty_invisible_template_fields(self):
        vals = {
            k: v
            for k, v in self._get_values_for_invisible_template_fields().items()
            if self[k] and self[k] != v
        }
        if vals:
            self.write(vals)

    @api.model
    def _get_values_for_invisible_template_fields(self):
        return {
            "date_start": False,
            "date_end": False,
            "date_deadline": False,
            "email_cc": False,
            "email_from": False,
            "kanban_state": "normal",
            "partner_id": False,
            "stage_id": False,
            "user_id": False,
        }

    @api.model
    def _search(self, args, *args_, **kwargs):
        """Hide templates from searches by default."""
        if should_apply_default_template_filter(args, self._context):
            args = AND((args or [], [("is_template", "=", False)]))
        return super()._search(args, *args_, **kwargs)

    @api.model
    def read_group(self, domain, *args, **kwargs):
        """Hide templates from grouped searches by default."""
        if should_apply_default_template_filter(domain, self._context):
            domain = AND((domain or [], [("is_template", "=", False)]))
        return super().read_group(domain, *args, **kwargs)


class ProjectTaskTemplatePropagationToSubtask(models.Model):
    """Integrate is_template with the concept of subtasks.

    Suppose a task is defined with subtasks.

    If we set the task as a template, then all its subtasks will becomme
    templates as well.
    """

    _inherit = "project.task"

    child_ids = fields.One2many(
        context={"active_test": False, SHOW_TASK_TEMPLATES: True}
    )

    def action_subtask(self):
        """Display child templates when clicking on the subtask smart button."""
        res = super().action_subtask()
        res["context"][SHOW_TASK_TEMPLATES] = True
        return res

    @api.onchange("parent_id")
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

        if "is_template" in vals:
            child_tasks = self.mapped("child_ids")
            if child_tasks:
                child_tasks.write({"is_template": vals["is_template"]})

        if vals.get("parent_id"):
            self._update_is_template_from_parent_task()

        return res

    @api.model
    def create(self, vals):
        task = super().create(vals)
        task._update_is_template_from_parent_task()
        return task


class ProjectTaskWithOriginTaskLink(models.Model):
    """Link a task with its origin template.

    This link allows to keep track of which template defined
    inside a project has a relative `effective` task.

    The relation is One2one. A task template on a project will
    generate one and only one task.
    """

    _inherit = "project.task"

    origin_template_id = fields.Many2one("project.task", "Origin Template", index=True)
    effective_task_ids = fields.One2many(
        "project.task",
        "origin_template_id",
        "Generated Tasks",
        context={"active_test": False},
    )

    _sql_constraints = [
        (
            "name_origin_template_id",
            "unique(origin_template_id)",
            "Only one task can be generated per template.",
        )
    ]


class ProjectTaskWithPivotTableLabel(models.Model):
    """Add a label to distinguish tasks from templates in the pivot view."""

    _inherit = "project.task"

    template_or_task = fields.Selection(
        [("1_template", "Template"), ("2_task", "Task")],
        "Template / Task",
        compute="_compute_template_or_task",
        store=True,
    )

    @api.depends("is_template")
    def _compute_template_or_task(self):
        for task in self:
            task.template_or_task = "1_template" if task.is_template else "2_task"
