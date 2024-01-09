# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import SavepointCase


class TestMeetingMinutesProjectParent(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.task_3 = cls.env["project.task"].create(
            {
                "project_id": cls.project_2.id,
                "name": "Task 3",
            }
        )

    def test_project_child_meeting_minutes(self):
        minutes_1 = (
            self.env["meeting.minutes.project"]
            .with_context(default_task_id=self.task_1.id)
            .create({})
        )
        minutes_1.on_change_task_id()
        minutes_2 = (
            self.env["meeting.minutes.project"]
            .with_context(default_task_id=self.task_2.id)
            .create({})
        )
        minutes_2.on_change_task_id()
        self.project_1.write({"parent_id": self.project_2.id})
        self.project_2._compute_nbr_meeting()
        assert 2 == self.project_2.meeting_minutes_count
        self.task_3.open_meeting_minutes()
        self.project_2._compute_nbr_meeting()
        assert 3 == self.project_2.meeting_minutes_count
