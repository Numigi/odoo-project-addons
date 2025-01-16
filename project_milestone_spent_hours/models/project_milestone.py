# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    total_hours = fields.Float(
        compute="_compute_total_hours",
        string="Total Hours",
        compute_sudo=True,
        store=True,
    )

    @api.depends(
        "task_ids",
        "task_ids.active",
        "task_ids.milestone_id",
        "task_ids.timesheet_ids",
        "task_ids.timesheet_ids.unit_amount",
        "active",
    )
    def _compute_total_hours(self):
        for record in self:
            total_hours = 0.0
            if record.active:
                total_hours = sum(
                    record.task_ids.filtered(lambda milestone: milestone.active)
                    .mapped("timesheet_ids")
                    .mapped("unit_amount")
                )
            record.total_hours = total_hours
