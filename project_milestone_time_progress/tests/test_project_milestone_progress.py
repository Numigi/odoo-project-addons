# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestMilestoneProgress(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project = cls.env["project.project"].create({"name": "My Project"})

        cls.milestone_1 = cls.env["project.milestone"].create(
            {"name": "My Milestone 1",
             "project_id": cls.project.id,
             "estimated_hours": 80.00}
        )

        cls.milestone_2 = cls.env["project.milestone"].create(
            {"name": "My Milestone 2", "project_id": cls.project.id}
        )

        cls.task_1 = cls.env["project.task"].create(
            {
                "name": "Task 1",
                "project_id": cls.project.id,
                "milestone_id": cls.milestone_1.id,
            }
        )

        cls.task_2 = cls.env["project.task"].create(
            {
                "name": "Task 2",
                "project_id": cls.project.id,
                "milestone_id": cls.milestone_2.id,
            }
        )

        cls.analytic_line_1 = cls.env["account.analytic.line"].create(
            {
                "name": "My Timesheet 1",
                "task_id": cls.task_1.id,
                "unit_amount": 20,
                "project_id": cls.project.id,
            }
        )

    def test_progress_calculation(self):
        self.assertEqual(self.milestone_1.progress, 25)

    # def test_show_progress_info(self):
    #     self.env["account.analytic.line"].create(
    #         {
    #             "name": "My Timesheet 2",
    #             "task_id": self.task_2.id,
    #             "unit_amount": 20,
    #             "project_id": self.project.id,
    #         }
    #     )
    #     self.assertEqual(self.milestone_2.show_progress_info_message, True)




