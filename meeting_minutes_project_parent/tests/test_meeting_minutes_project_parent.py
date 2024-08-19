# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import SavepointCase


class TestMeetingMinutesProjectParent(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_1 = cls.env["project.project"].create(
            {"name": "Project 1"}
        )
        cls.project_2 = cls.env["project.project"].create(
            {"name": "Project 2", "parent_id": cls.project_1.id}
        )

        cls.MeetingMinutesObj = cls.env["meeting.minutes.project"]

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
        cls.task_3 = cls.env["project.task"].create(
            {
                "project_id": cls.project_2.id,
                "name": "Task 3",
            }
        )

    def test_project_child_meeting_minutes(self):
        self.MeetingMinutesObj.create({
                'task_id': self.task_1.id,
                'project_id': self.project_1.id,
            })
        self.MeetingMinutesObj.create({
                'task_id': self.task_2.id,
                'project_id': self.project_1.id,
            })
        self.MeetingMinutesObj.create({
                'task_id': self.task_2.id,
                'project_id': self.project_2.id
            })
        assert self.project_1.meeting_minutes_count == 3
        assert self.project_2.meeting_minutes_count == 1
