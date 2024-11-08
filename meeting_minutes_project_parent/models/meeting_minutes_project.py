# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MeetingMinutesProject(models.Model):
    _inherit = "meeting.minutes.project"

    parent_project_id = fields.Many2one(
        "project.project",
        string="Parent Project",
        compute="_compute_parent_project_id",
        store=True,
    )

    @api.depends("project_id", "project_id.parent_id")
    def _compute_parent_project_id(self):
        for record in self:
            record.parent_project_id = (
                record.project_id.parent_id if record.project_id and
                record.project_id.parent_id else False
            )
