# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, models, fields


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    remaining_hours = fields.Float(compute='_compute_remaining_hours', string="Remaining Hours", store=True, readonly=True)


    @api.depends("estimated_hours", "total_hours")
    def _compute_remaining_hours(self):
        for rec in self:
            rec.remaining_hours = rec.estimated_hours - rec.total_hours
