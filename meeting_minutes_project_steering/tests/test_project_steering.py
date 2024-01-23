# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.meeting_minutes_project.tests.test_project_meeting_minutes import (
    TestMeetingMinutesProject,
)


class TestProjectSteering(TestMeetingMinutesProject):
    @classmethod
    def setUpClass(cls):
        super(TestProjectSteering, cls).setUpClass()
        task_model = cls.env["ir.model"].search([("model", "=", "project.task")]).id
        cls.steering_kpi_1 = cls.env["project.steering.kpi"].create(
            {
                "name": "Steering KPI 1",
                "sequence": 2,
                "model_id": task_model,
                "filter_domain": '["&",["name","ilike","Room"],["user_id","!=",False]]',
            }
        )

        cls.steering_kpi_2 = cls.env["project.steering.kpi"].create(
            {
                "name": "Steering KPI 2",
                "sequence": 1,
                "model_id": task_model,
                "filter_domain": '["&",["date_deadline","<","2024-01-03"],["date_deadline","!=",False]]',
            }
        )

        cls.steering_kpi_3 = cls.env["project.steering.kpi"].create(
            {
                "name": "Steering KPI 3",
                "sequence": 3,
                "model_id": task_model,
                "filter_domain": '[["planned_hours",">=",4]]',
            }
        )

        cls.steering_kpi_4 = cls.env["project.steering.kpi"].create(
            {
                "name": "Steering KPI 4",
                "sequence": 5,
                "active": False,
                "model_id": task_model,
                "filter_domain": "[]",
            }
        )

        cls.task_3 = cls.env["project.task"].create(
            {
                "project_id": cls.project_1.id,
                "name": "Room Task 3",
                "planned_hours": 5,
            }
        )

        cls.task_4 = cls.env["project.task"].create(
            {
                "project_id": cls.project_1.id,
                "name": "Room Task 4",
                "planned_hours": 2,
                "date_deadline": "2024-01-02",
            }
        )

    def test_project_steering_load_data(self):
        self.task_1.planned_hours = 7
        self.task_1.name = "Room Task 1"
        self.task_2.date_deadline = "2024-01-01"

        minutes = self._create_minutes()

        minutes.project_steering_enabled = True
        minutes.load_steering_data()
        minutes.refresh()

        # Expected results (3 sections + 7 task lines = 10 lines):
        # > Steering KPI 2 (0)
        # >>> task_4
        # >>> task_2
        # > Steering KPI 1 (3)
        # >>> task_3
        # >>> task_4
        # >>> task_1
        # > Steering KPI 3 (7)
        # >>> task_3
        # >>> task_1

        self.assertTrue(minutes.project_id)

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
        self.assertEqual(len(minutes.project_steering_ids.ids), 10)
        # The order of section must be with the following order
        self.assertEqual(minutes.project_steering_ids[0].name, "Steering KPI 2")
        self.assertEqual(minutes.project_steering_ids[3].name, "Steering KPI 1")
        self.assertEqual(minutes.project_steering_ids[7].name, "Steering KPI 3")
