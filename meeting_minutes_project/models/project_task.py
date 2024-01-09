# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    mentions_count = fields.Integer(string="Mentions", compute="_compute_mentions")
    meeting_minutes_ids = fields.One2many(
        "meeting.minutes.project",
        "task_id",
        string="Meeting minutes associated to this task",
    )
    meeting_minutes_count = fields.Integer(
        string="Meeting minutes",
        compute="_compute_nbr_meetings",
        groups="project.group_project_user",
    )

    @api.multi
    def _compute_nbr_meetings(self):
        for task in self:
            task.meeting_minutes_count = len(task.meeting_minutes_ids)

    @api.multi
    def _compute_mentions(self):
        for task in self:
            mentions_ids = self.env["meeting.minutes.discuss.point"].search(
                [("task_id", "=", task.id)]
            )
            task.mentions_count = len(mentions_ids)
