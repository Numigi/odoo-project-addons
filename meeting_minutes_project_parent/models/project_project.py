# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.multi
    def _compute_nbr_meeting(self):
        super()._compute_nbr_meeting()
        for project in self:
            if project.child_ids:
                project.meeting_minutes_project_ids = self.env[
                    "meeting.minutes.project"
                ].search(
                    [
                        "|",
                        ("parent_project_id", "=", project.id),
                        ("project_id", "=", project.id),
                    ]
                )
                project.meeting_minutes_count = len(project.meeting_minutes_project_ids)
