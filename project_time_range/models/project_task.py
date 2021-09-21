# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from .util import time_range_constraint


class ProjectTask(models.Model):

    _inherit = "project.task"

    min_hours = fields.Float("Minimum Planned Hours")
    max_hours = fields.Float("Maximum Planned Hours")
    planned_hours = fields.Float(string="Ideal Planned Hours")

    subtask_min_hours = fields.Float(
        "Sub-tasks Min", compute="_compute_subtask_min_hours"
    )
    subtask_max_hours = fields.Float(
        "Sub-tasks Max", compute="_compute_subtask_max_hours"
    )

    def _compute_subtask_min_hours(self):
        for task in self:
            task.subtask_min_hours = sum(task.child_ids.mapped("min_hours"))

    def _compute_subtask_max_hours(self):
        for task in self:
            task.subtask_max_hours = sum(task.child_ids.mapped("max_hours"))

    @api.constrains("planned_hours", "max_hours")
    @time_range_constraint
    def _check_max_hours(self):
        if self.max_hours < self.planned_hours:
            raise ValidationError(
                _("Max Hours must be greater than the planned hours.")
            )

    @api.constrains("planned_hours", "min_hours")
    @time_range_constraint
    def _check_min_hours(self):
        if self.min_hours > self.planned_hours:
            raise ValidationError(_("Min Hours must be lesser than the planned hours."))

    @api.constrains("planned_hours", "min_hours", "max_hours")
    @time_range_constraint
    def _check_positive_hours(self):
        if any(h < 0 for h in [self.min_hours, self.planned_hours, self.max_hours]):
            raise ValidationError(_("Hours must be positive numbers."))

    @api.model
    def create(self, vals):
        if "max_hours" not in vals:
            vals["max_hours"] = vals.get("planned_hours")
        return super().create(vals)
