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

    def get_meeting_minutes(self):
        minutes = self.env["meeting.minutes.project"].search(
            [("task_id", "=", self.id)]
        )
        if not minutes:
            minutes = self._create_meeting_minutes()
        return minutes

    def _create_meeting_minutes(self):
        return self.env["meeting.minutes.project"].create(
            self._get_meeting_minutes_vals()
        )

    def _get_meeting_minutes_vals(self):
        partner_follower_ids = self.message_follower_ids.filtered(
            lambda f: f.partner_id and not f.channel_id and not f.partner_id.is_company
        )
        return {
            "preview_point": self.description,
            "task_id": self.id,
            "partner_ids": [
                (
                    6,
                    0,
                    [follower.partner_id.id for follower in partner_follower_ids],
                )
            ],
        }

    def open_meeting_minutes(self):
        meeting_minutes_id = self.get_meeting_minutes()
        if len(meeting_minutes_id) > 1:
            action = self.env.ref(
                "meeting_minutes_project.action_view_task_meeting_minutes"
            ).read()[0]
            return action
        return {
            "name": "Meeting Minutes",
            "view_type": "form",
            "view_mode": "form",
            "view_id": self.env.ref(
                "meeting_minutes.meeting_minutes_view_mixin_form"
            ).id,
            "res_model": "meeting.minutes.project",
            "res_id": meeting_minutes_id.id,
            "type": "ir.actions.act_window",
            "target": "current",
        }
