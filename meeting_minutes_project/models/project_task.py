# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    mentions_count = fields.Integer(string="Mentions", compute="_compute_mentions")
    task_meeting_minutes_ids = fields.Many2many(
        "meeting.minutes.project",
        compute="_compute_meeting_minutes_project",
        string="Meeting minutes associated to this task",
    )
    task_meeting_minutes_count = fields.Integer(
        string="Meeting minutes",
        compute="_compute_meeting_minutes_project",
        groups="project.group_project_user",
    )

    @api.multi
    def _compute_meeting_minutes_project(self):
        for task in self:
            task.task_meeting_minutes_ids = self.env["meeting.minutes.project"].search(
                [
                    ("task_id", "=", task.id),
                ]
            )
            task.task_meeting_minutes_count = len(task.task_meeting_minutes_ids)

    @api.multi
    def _compute_mentions(self):
        for task in self:
            mentions_ids = self.env["meeting.minutes.discuss.point"].search(
                [("task_id", "=", task.id)]
            )
            task.mentions_count = len(mentions_ids)
