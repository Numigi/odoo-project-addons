# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from datetime import timedelta
from pytz import timezone
from odoo import fields
from odoo.tests.common import SavepointCase


class TestMeetingMinutesProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner 1",
                "email": "partner1@yourcompany.com",
            }
        )
        cls.channel = cls.env["mail.channel"].create({"name": "Channel 1"})

        cls.project_1 = cls.env["project.project"].create({"name": "Project 1"})
        cls.project_2 = cls.env["project.project"].create({"name": "Project 2"})

        cls.task_1 = cls.env["project.task"].create(
            {
                "project_id": cls.project_1.id,
                "name": "Task 1",
            }
        )

        cls.task_2 = cls.env["project.task"].create(
            {
                "project_id": cls.project_1.id,
                "name": "Task 2",
            }
        )

        cls.today = fields.Date.context_today(cls.task_1)
        cls.yesterday = cls.today - timedelta(1)

    def test_open_meeting_minutes(self):
        minutes = self.task_1.open_meeting_minutes()
        assert (
            minutes.get("view_id", False)
            == self.env.ref("meeting_minutes.meeting_minutes_view_mixin_form").id
        )

    def test_second_click_open_meeting_minutes(self):
        action = self.task_2.open_meeting_minutes()
        action_2 = self.task_2.open_meeting_minutes()
        assert action["res_id"] == action_2["res_id"]

    def test_task_partner_follower_in_participants(self):
        self.task_1._message_subscribe(self.partner.ids)
        minutes = self._create_minutes()
        assert self.partner in minutes.partner_ids

    def test_task_commercial_follower_not_in_participants(self):
        self.partner.is_company = True
        self.task_1._message_subscribe(self.partner.ids)
        minutes = self._create_minutes()
        assert self.partner not in minutes.partner_ids

    def test_task_channel_follower_in_participants(self):
        self.task_1._message_subscribe(self.partner.ids)
        self.task_1._message_subscribe([], self.channel.ids)
        minutes = self._create_minutes()
        minutes.discuss_point_ids.create(
            {
                "meeting_minutes_id": minutes.id,
                "sequence": 0,
                "task_id": self.task_1.id,
                "notes": "My notes",
            }
        )
        assert self.channel.id not in minutes.partner_ids.ids
        assert self.project_1.meeting_minutes_project_count == 1
        assert self.task_1.mentions_count == 1
        assert self.task_1.task_meeting_minutes_count == 1

    def test_meeting_minutes_display_name(self):
        minutes = self._create_minutes()
        date = minutes.create_date.astimezone(timezone(self.env.user.tz))
        expected_name = "Meeting Minutes: {task} - {create_datetime}".format(
            task=self.task_1.display_name,
            create_datetime=date.strftime("%Y-%m-%d %H:%M:%S"),
        )

        assert minutes.display_name == expected_name

    def test_homework_activity_in_waiting_actions(self):
        activity = self._create_homework_activity(self.yesterday)
        minutes = self._create_minutes()
        assert activity in minutes.action_ids

    def test_different_project_homework_activity_not_in_waiting_actions(self):
        activity = self._create_homework_activity(self.yesterday)
        self.task_2.write({"project_id": self.project_2.id})
        minutes = self._create_minutes()
        assert activity not in minutes.action_ids

    def test_meeting_activity_not_in_waiting_actions(self):
        activity = self._create_meeting_activity()
        minutes = self._create_minutes()
        assert activity not in minutes.action_ids

    def test_closed_homework_activity_not_in_waiting_actions(self):
        activity = self._create_homework_activity(self.yesterday)
        activity.action_done()
        minutes = self._create_minutes()
        assert activity not in minutes.action_ids

    def test_today_homework_activity_not_in_waiting_actions(self):
        activity = self._create_homework_activity(self.today)
        minutes = self._create_minutes()
        assert activity not in minutes.action_ids

    def _create_minutes(self):
        self.env["meeting.minutes.project"].search(
            [("task_id", "=", self.task_1.id)]
        ).unlink()
        meeting_minutes = self.task_1.open_meeting_minutes()
        minutes = self.env["meeting.minutes.project"].search(
            [("id", "=", meeting_minutes.get("res_id", False))]
        )
        return minutes

    def _create_homework_activity(self, date_deadline):
        mail_activity = self.env["mail.activity"].create(
            {
                "res_id": self.task_2.id,
                "res_model": "project.task",
                "user_id": self.env.ref("base.user_admin").id,
                "date_deadline": date_deadline,
                "activity_type_id": self.env.ref(
                    "meeting_minutes_project.activity_homework"
                ).id,
                "res_model_id": self.env.ref("project.model_project_task").id,
            }
        )
        return mail_activity

    def _create_meeting_activity(self):
        return self.env["mail.activity"].create(
            {
                "res_id": self.task_2.id,
                "res_model": "project.task",
                "user_id": self.env.ref("base.user_admin").id,
                "date_deadline": fields.Date.today(),
                "activity_type_id": self.env.ref("mail.mail_activity_data_meeting").id,
                "res_model_id": self.env.ref("project.model_project_task").id,
            }
        )
