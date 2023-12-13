# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    projected_hours = fields.Float(
        "Projected Hours",
        compute="_compute_project_data",
        store=True,
    )
    real_progress = fields.Float(
        "Real Progress",
        digits=(16, 2),
        compute="_compute_project_data",
        store=True,
    )

    @api.depends("effective_hours", "remaining_hours")
    def _compute_project_data(self):
        """Compute projected hours and real progress."""
        for task in self:
            effective_hours, remaining_hours = (
                task.effective_hours,
                task.remaining_hours,
            )
            projected_hours = effective_hours + remaining_hours
            task.projected_hours = projected_hours
            task.real_progress = 100.0 * effective_hours / projected_hours\
                if projected_hours else 0.0
