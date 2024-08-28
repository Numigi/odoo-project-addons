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

    @api.depends("project_id" , "project_id.parent_id")
    def _compute_parent_project_id(self):
        for record in self:
            record.parent_project_id = (
                record.project_id.parent_id if record.project_id else False
            )

    @api.onchange("project_id")
    def on_change_project_id(self):
        super().on_change_project_id()
        if self.project_id:
            self.parent_project_id = self.project_id.parent_id.id

    @api.onchange("parent_project_id")
    def on_change_parent_project_id(self):
        if self.parent_project_id and not self.project_id:
            self._set_document_ref(self.parent_project_id, "project.project")
            self._set_meeting_minutes_name(self.parent_project_id)
