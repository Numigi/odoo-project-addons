# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Project(models.Model):
    _inherit = "project.project"

    budget_min_hours = fields.Float(
        "Minimum Budgeted Hours", compute="_compute_time_range", store=True
    )
    budget_max_hours = fields.Float(
        "Maximum Budgeted Hours", compute="_compute_time_range", store=True
    )
    budget_planned_hours = fields.Float(
        string="Ideal Budgeted Hours", compute="_compute_time_range", store=True
    )
    budget_remaining_hours = fields.Float(
        string="Remaining Budgeted Hours",
        compute="_compute_budget_remaining_hours"
    )

    @api.depends("task_ids.is_template")
    def _compute_time_range(self):
        super()._compute_time_range()
        for project in self:
            tasks = project._get_parent_template_tasks()
            project.budget_min_hours = sum(tasks.mapped("min_hours"))
            project.budget_max_hours = sum(tasks.mapped("max_hours"))
            project.budget_planned_hours = sum(tasks.mapped("planned_hours"))

    def _get_parent_template_tasks(self):
        return self.env["project.task"].search(
            [
                ("project_id", "=", self.id),
                ("parent_id", "=", False),
                ("is_template", "=", True),
            ]
        )

    def _compute_budget_remaining_hours(self):
        for project in self:
            project.budget_remaining_hours = (
                    project.budget_planned_hours - project.consumed_hours
            )
