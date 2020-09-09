# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTaskWithMinAndMaxHours(models.Model):
    """Add the fields min_hours and max_hours on tasks."""

    _inherit = 'project.project'

    min_hours = fields.Float('Minimum Planned Hours', compute="_compute_min_hours", store=True, track_visibility="onchange")
    max_hours = fields.Float('Maximum Planned Hours', compute="_compute_max_hours", store=True, track_visibility="onchange")
    planned_hours = fields.Float(string='Ideal Planned Hours', compute="_compute_planned_hours", store=True, track_visibility="onchange")

    @api.one
    @api.constrains('planned_hours', 'min_hours', 'max_hours')
    def _check_description(self):
        if self.planned_hours > 0:
            if self.min_hours > self.planned_hours:
                raise ValidationError(
                    _("Min Hours must be lesser than the planned hours.")
                )
            elif self.max_hours < self.planned_hours:
                raise ValidationError(
                    _("Max Hours must be greater than the planned hours.")
                )

    @api.depends("task_ids", "task_ids.is_template", "task_ids.min_hours")
    def _compute_min_hours(self):
        for record in self:
            record.min_hours = record.get_total_template_task_amount("min_hours")

    @api.depends("task_ids", "task_ids.is_template", "task_ids.max_hours")
    def _compute_max_hours(self):
        for record in self:
            record.max_hours = record.get_total_template_task_amount("max_hours")

    @api.depends("task_ids", "task_ids.is_template", "task_ids.planned_hours")
    def _compute_planned_hours(self):
        for record in self:
            record.planned_hours = record.get_total_template_task_amount("planned_hours")

    @api.multi
    def get_total_template_task_amount(self, task_field):
        self.ensure_one()
        return sum(
            self.with_context(show_task_templates=True).task_ids
                .filtered(lambda t: t.is_template).mapped(task_field)
        )
