# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from pytz import timezone
from odoo import fields, models, api, _


class MeetingMinutesProject(models.Model):
    _name = "meeting.minutes.project"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"meeting.minutes.mixin": "meeting_minute_id"}

    task_id = fields.Many2one(
        "project.task",
        string="Task",
        ondelete="restrict",
    )
    project_id = fields.Many2one(
        "project.project",
        string="Project",
    )
    meeting_minute_id = fields.Many2one(
        "meeting.minutes.mixin",
        string='Meeting Minute',
        required=True,
        ondelete='cascade'
    )
    discuss_point_ids = fields.One2many(
        "meeting.minutes.discuss.point",
        "meeting_minutes_id",
        string="Discussed Points"
    )
    action_ids = fields.One2many(
        "mail.activity",
        compute="_compute_action_ids",
        string="Actions", readonly=True
    )
    homework_ids = fields.One2many(
        "mail.activity",
        "meeting_minutes_id",
        string="Homework"
    )

    def _set_meeting_minutes_name(self, record):
        self.ensure_one()
        name_format = _("Meeting Minutes: {record_name} - {create_datetime}")
        create_date = self.create_date or datetime.today()
        create_date = create_date.astimezone(timezone(self.env.user.tz))
        self.name = name_format.format(
            record_name=record.display_name,
            create_datetime=create_date.strftime("%Y-%m-%d %H:%M:%S"),
        )

    def _set_document_ref(self, record, model):
        self.ensure_one()
        self.res_id = record.id
        self.res_model = model

    def _set_attendees(self, record):
        self.ensure_one()
        # Filter odoobot to avoid displaying it on edit mode then disappear on save
        odoobot_id = self.env.ref("base.partner_root")
        partner_follower_ids = record.message_follower_ids.filtered(
                lambda f: f.partner_id
                and not f.channel_id
                and not f.partner_id.is_company
                and f.partner_id.id != odoobot_id
            )
        self.partner_ids = [
            (6, 0, [follower.partner_id.id for follower in partner_follower_ids])
        ]

    @api.onchange("task_id")
    def on_change_task_id(self):
        if self.task_id:
            self._set_attendees(self.task_id)
            self.project_id = self.task_id.project_id.id
            self._set_document_ref(self.task_id, "project.task")
            self._set_meeting_minutes_name(self.task_id)

    @api.onchange("project_id")
    def on_change_project_id(self):
        if self.project_id and not self.task_id:
            self._set_attendees(self.project_id)
            self._set_document_ref(self.project_id, "project.project")
            self._set_meeting_minutes_name(self.project_id)

    @api.multi
    def _compute_action_ids(self):
        homework = self.env.ref("meeting_minutes_project.activity_homework")
        today = fields.Date.context_today(self)
        for rec in self:
            activities = self.env["mail.activity"].search([
                ("res_model", "=", "project.task"),
                ("res_id", "in", rec.project_id.task_ids.ids),
                ("activity_type_id", "=", homework.id),
                ("date_deadline", "<", today),
            ])
            rec.action_ids = activities
