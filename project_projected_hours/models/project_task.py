# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    projected_hours = fields.Float(
        "Projected Hours",
        compute="_compute_projected_hours",
        readonly=True,
        store=True,
    )
    real_progress = fields.Float(
        "Real Progress",
        digits=(16, 2),
        compute="_compute_real_progress",
        readonly=True,
        store=True,
    )
    progress_variance = fields.Float(
        "Progress Variance",
        digits=(16, 2),
        compute="_compute_progress_variance",
        readonly=True,
        store=True,
    )

    @api.depends("effective_hours", "remaining_hours")
    def _compute_projected_hours(self):
        for task in self:
            task.projected_hours = task.effective_hours + task.remaining_hours

    @api.depends("effective_hours", "remaining_hours")
    def _compute_real_progress(self):
        for task in self:
            projected_hours = task.effective_hours + task.remaining_hours
            if projected_hours:
                task.real_progress = task.effective_hours / projected_hours
            else:
                task.real_progress = 0

    @api.depends("progress", "real_progress")
    def _compute_progress_variance(self):
        for task in self:
            task.real_progress = task.real_progress - task.progress
