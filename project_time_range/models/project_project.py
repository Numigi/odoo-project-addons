# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    min_hours = fields.Float(
        "Minimum Planned Hours", compute="_compute_time_range", store=True
    )
    max_hours = fields.Float(
        "Maximum Planned Hours", compute="_compute_time_range", store=True
    )
    planned_hours = fields.Float(
        string="Ideal Planned Hours", compute="_compute_time_range", store=True
    )
    consumed_hours = fields.Float(
        string="Consumed Hours", compute="_compute_consumed_remaining_hours"
    )
    remaining_hours = fields.Float(
        string="Remaining Hours", compute="_compute_consumed_remaining_hours"
    )

    @api.depends(
        "task_ids",
        "task_ids.min_hours",
        "task_ids.max_hours",
        "task_ids.planned_hours",
        "task_ids.active",
        "task_ids.parent_id",
    )
    def _compute_time_range(self):
        for project in self:
            tasks = project._get_parent_tasks()
            project.min_hours = sum(tasks.mapped("min_hours"))
            project.max_hours = sum(tasks.mapped("max_hours"))
            project.planned_hours = sum(tasks.mapped("planned_hours"))

    def _get_parent_tasks(self):
        return (
            self.env["project.task"]
            .with_context({})
            .search([("project_id", "=", self.id), ("parent_id", "=", False)])
        )

    def _compute_consumed_remaining_hours(self):
        consumed_hours = self._get_consumed_hours_per_project()
        for project in self:
            project.consumed_hours = consumed_hours.get(project.id, 0)
            project.remaining_hours = project.planned_hours - project.consumed_hours

    def _get_consumed_hours_per_project(self):
        self._cr.execute(
            "SELECT project_id, sum(unit_amount) "
            "FROM account_analytic_line "
            "WHERE project_id in %s "
            "GROUP BY project_id",
            (tuple(self.ids),),
        )
        return dict(self._cr.fetchall())
