# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from pytz import timezone
from odoo import fields, models, api, _


class MeetingMinutesProject(models.Model):
    _name = "meeting.minutes.project"
    _inherit = ["mail.thread", "mail.activity.mixin", "meeting.minutes.mixin"]

    name = fields.Char(compute="_compute_name")
    task_id = fields.Many2one(
        "project.task", string="Task", ondelete="restrict", index=True, store=True
    )
    project_id = fields.Many2one(
        "project.project",
        related="task_id.project_id",
        string="Project",
        readonly=True,
        store=True,
    )
    action_ids = fields.One2many(
        "mail.activity", compute="_compute_action_ids", string="Actions", readonly=True
    )
    discuss_point_ids = fields.One2many(
        "meeting.minutes.discuss.point", "meeting_minutes_id", string="Discussed Points"
    )
    homework_ids = fields.One2many(
        "mail.activity", "meeting_minutes_id", string="Homework"
    )

    @api.onchange("task_id")
    def on_change_task_id(self):
        # Filter odoobot to avoid displaying it on edit mode then disappear on save
        odoobot_id = self.env["ir.model.data"].xmlid_to_res_id("base.partner_root")
        partner_follower_ids = self.task_id.message_follower_ids.filtered(
            lambda f: f.partner_id
            and not f.channel_id
            and not f.partner_id.is_company
            and f.partner_id.id != odoobot_id
        )
        self.partner_ids = [
            (
                6,
                0,
                [follower.partner_id.id for follower in partner_follower_ids],
            )
        ]

    def _compute_name(self):
        name_format = _("Meeting Minutes: {task} - {create_datetime}")
        for record in self:
            date = record.create_date.astimezone(timezone(self.env.user.tz))
            record.name = name_format.format(
                task=record.task_id.display_name,
                create_datetime=date.strftime("%Y-%m-%d %H:%M:%S"),
            )

    @api.multi
    def _compute_action_ids(self):
        homework = self.env.ref("meeting_minutes_project.activity_homework")
        today = fields.Date.context_today(self)

        for rec in self:
            activities = self.env["mail.activity"].search(
                [("res_id", "in", rec.task_id.project_id.task_ids.ids)],
            )
            rec.action_ids = activities.filtered(
                lambda a: (
                    a.activity_type_id == homework
                    and a.res_model == "project.task"
                    and a.date_deadline < today
                )
            )
