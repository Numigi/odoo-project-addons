# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    color = fields.Char("Color", compute="_compute_milestone_color")

    def _compute_milestone_color(self):
        for record in self:
            color = '#FFFFFF'
            if record.type_id and record.type_id.html_color \
                    and record.type_id.active:
                color = record.type_id.html_color
            record.color = color
