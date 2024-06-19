# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.meeting_minutes_project_steering.tests.test_project_steering import (
    TestProjectSteering,
)


class TestProjectParentSteering(TestProjectSteering):
    def setUp(self):
        super().setUp()
        self.project_2 = self.env["project.project"].create({"name": "Project 2"})
        self.project_parent = self.env["project.project"].create(
            {"name": "Project Parent"}
        )

    def test_steering_from_project_parent(self):
        self.project_2.parent_id = self.project_parent.id
        self.project_1.parent_id = self.project_parent.id

        self.task_2_1 = self.env["project.task"].create(
            {
                "project_id": self.project_2.id,
                "name": "Task 2-1",
                "planned_hours": 7,
            }
        )

        self.task_2_2 = self.env["project.task"].create(
            {
                "project_id": self.project_2.id,
                "name": "Room Task 2-2",
                "date_deadline": "2024-01-01",
            }
        )

        minutes = self._new_minutes()
        self.project_parent.refresh()

        minutes.project_steering_enabled = True
        minutes.load_steering_data()
        minutes.refresh()

        # Three sections to have
        self.assertEqual(
            len(
                minutes.project_steering_ids.filtered(
                    lambda t: t.display_type == "line_section"
                ).ids
            ),
            3,
        )
        # Total of lines
        self.assertEqual(len(minutes.project_steering_ids.ids), 13)

    def _new_minutes(self):
        self.env["meeting.minutes.project"].search(
            [("task_id", "=", self.task_2_1.id)]
        ).unlink()

        minutes = (
            self.env["meeting.minutes.project"]
            .with_context(default_task_id=self.task_2_1.id)
            .create({})
        )
        minutes.on_change_task_id()
        return minutes
