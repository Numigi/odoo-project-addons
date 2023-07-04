# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    progress_variance = fields.Float(
        "Progress Variance",
        digits=(16, 2),
        compute="_compute_progress_variance",
        readonly=True,
        store=True,
    )

    @api.depends("progress", "real_progress")
    def _compute_progress_variance(self):
        for task in self:
            task.progress_variance = task.real_progress - task.progress
