# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    meeting_minutes_ids = fields.One2many(
        "meeting.minutes.project",
        "project_id",
        string="Meeting minutes associated to this project",
    )
    meeting_minutes_count = fields.Integer(
        string="Meeting minutes",
        compute="_compute_nbr_meeting",
    )

    @api.multi
    def _compute_nbr_meeting(self):
        for project in self:
            project.meeting_minutes_count = len(
                project.meeting_minutes_ids
            )
