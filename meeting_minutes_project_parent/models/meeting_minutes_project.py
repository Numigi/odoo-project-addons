# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MeetingMinutesProject(models.Model):
    _inherit = "meeting.minutes.project"

    parent_project_id = fields.Many2one(
        "project.project", string="Parent Project", related="project_id.parent_id"
    )
