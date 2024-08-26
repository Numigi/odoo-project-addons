# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DiscussPoint(models.Model):
    _name = "meeting.minutes.discuss.point"
    _description = "Discussed Points"
    _rec_name = "task_id"
    _order = "sequence"

    meeting_minutes_id = fields.Many2one(
        "meeting.minutes.project",
        string="Meeting Minutes",
        ondelete="cascade"
    )
    sequence = fields.Integer(string="Sequence")
    task_id = fields.Many2one(
        "project.task",
        string="Task",
        ondelete="restrict"
    )
    notes = fields.Html(string="Notes")
