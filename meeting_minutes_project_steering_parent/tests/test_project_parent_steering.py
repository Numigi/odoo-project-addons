# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License: AGPL-3.0 or later. See http://www.gnu.org/licenses/agpl

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

        # Kpi indicator for project
        self.steering_kpi_project = self.env["project.steering.kpi"].create(
            {
                "name": "Steering KPI Project",
                "sequence": 6,
                "model_id": self.env.ref("project.model_project_project").id,
                "primary_filter_domain": '[["name","ilike","Project"]]',
            }
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
        minutes.action_load_steering_data()
        minutes.refresh()

        # Four sections to have
        # 1 for project and 3 for tasks
        self.assertEqual(
            len(
                minutes.project_steering_ids.filtered(
                    lambda t: t.display_type == "line_section"
                ).ids
            ),
            4,
        )
        # Total of lines
        self.assertEqual(len(minutes.project_steering_ids.ids), 17)

        # Test few project name for each project_steering_ids
        # linked to the project_parent
        self.assertEqual(
            minutes.project_steering_ids[1].name, "Project Parent, Project 2"
        )
        self.assertEqual(
            minutes.project_steering_ids[2].name, "Project Parent, Project 1"
        )
        self.assertEqual(
            minutes.project_steering_ids[3].name, "Project Parent, Project 1"
        )

    def _new_minutes(self):
        minutes = (
            self.env["meeting.minutes.project"]
            .with_context(default_task_id=self.task_2_1.id)
            .create({})
        )
        minutes.on_change_task_id()
        return minutes
