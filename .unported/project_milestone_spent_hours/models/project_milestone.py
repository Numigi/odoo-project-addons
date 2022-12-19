# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    total_hours = fields.Float(
        compute="_get_total_hours", string="Total Hours", compute_sudo=True, store=True
    )

    @api.multi
    @api.depends(
        "project_task_ids",
        "project_task_ids.active",
        "project_task_ids.milestone_id",
        "project_task_ids.timesheet_ids",
        "project_task_ids.timesheet_ids.unit_amount",
        "active",
    )
    def _get_total_hours(self):
        for record in self.filtered(lambda milestone: milestone.active):
            record.total_hours = sum(
                record.project_task_ids.filtered(lambda milestone: milestone.active)
                .mapped("timesheet_ids")
                .mapped("unit_amount")
            )
