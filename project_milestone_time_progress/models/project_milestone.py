# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    progress = fields.Float(
        compute="_compute_milestone_progress",
        store=True,
        help="The Progress Percentage represents the Total"
             " Hours vs the Planned Hours of the Milestone.")
    show_progress_info_message = fields.Boolean()

    @api.depends('estimated_hours', 'total_hours')
    def _compute_milestone_progress(self):
        progress = 0.0
        show_info_message = False
        for record in self:
            if record.estimated_hours:
                progress = round(
                    (record.total_hours / record.estimated_hours) * 100, 2)
            else:
                show_info_message = True
            record.progress = progress
            record.show_progress_info_message = show_info_message
