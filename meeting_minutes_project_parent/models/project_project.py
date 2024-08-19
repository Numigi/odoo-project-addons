# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    def _compute_nbr_meeting(self):
        super()._compute_nbr_meeting()
        for project in self:
            if project.is_parent:
                meeting_minutes_childs_count = sum(
                    project.child_ids.mapped("meeting_minutes_count")
                )
                meeting_minutes_parent_count = len(project.meeting_minutes_ids)
                project.meeting_minutes_count = (
                    meeting_minutes_childs_count + meeting_minutes_parent_count
                )
