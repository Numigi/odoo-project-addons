# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    total_progress = fields.Float(
        "Total Progress",
        digits=(16, 2),
        compute="_compute_total_progress",
        readonly=True,
        store=True,
    )

    total_real_progress = fields.Float(
        "Total Real Progress",
        digits=(16, 2),
        compute="_compute_total_real_progress",
        readonly=True,
        store=True,
    )

    total_progress_variance = fields.Float(
        "Total Progress Variance",
        digits=(16, 2),
        compute="_compute_total_progress_variance",
        readonly=True,
        store=True,
    )

    @api.depends("tasks", "tasks.planned_hours", "tasks.effective_hours")
    def _compute_total_progress(self):
        for project in self:
            planned_hours = sum(project.tasks.mapped("planned_hours"))
            effective_hours = sum(project.tasks.mapped("effective_hours"))
            project.total_progress = (
                100.0 * (effective_hours / planned_hours) if planned_hours else 0.0
            )

    @api.depends("tasks", "tasks.projected_hours", "tasks.effective_hours")
    def _compute_total_real_progress(self):
        for project in self:
            projected_hours = sum(project.tasks.mapped("projected_hours"))
            effective_hours = sum(project.tasks.mapped("effective_hours"))
            project.total_real_progress = (
                100.0 * (effective_hours / projected_hours) if projected_hours else 0.0
            )

    @api.depends("total_progress", "total_real_progress")
    def _compute_total_progress_variance(self):
        for project in self:
            project.total_progress_variance = (
                project.total_real_progress - project.total_progress
            )
