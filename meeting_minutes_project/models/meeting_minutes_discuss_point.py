# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DiscussPoint(models.Model):
    _name = "meeting.minutes.discuss.point"
    _description = "Discuss Points"
    _rec_name = "minutes_task_id"

    meeting_minutes_id = fields.Many2one(
        "meeting.minutes.project", string="Meeting Minutes"
    )
    sequence = fields.Integer(string="Sequence")
    task_id = fields.Many2one("project.task", ondelete="restrict")
    minutes_task_id = fields.Many2one(
        "project.task",
        related="meeting_minutes_id.task_id",
        string="Meeting Minutes Task",
    )
    notes = fields.Html(string="Notes")
