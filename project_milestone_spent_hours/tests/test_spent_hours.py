# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestMilestoneTotalHours(TransactionCase):
    def setUp(self):
        super().setUp()

        self.project = self.env["project.project"].create({"name": "My Project"})

        self.milestone_1 = self.env["project.milestone"].create(
            {"name": "My Milestone 1", "project_id": self.project.id}
        )

        self.milestone_2 = self.env["project.milestone"].create(
            {"name": "My Milestone 2", "project_id": self.project.id}
        )

        self.task = self.env["project.task"].create(
            {
                "name": "My Task",
                "project_id": self.project.id,
                "milestone_id": self.milestone_1.id,
            }
        )

        self.analytic_line_1 = self.env["account.analytic.line"].create(
            {
                "name": "My Timesheet 1",
                "task_id": self.task.id,
                "unit_amount": 10,
                "project_id": self.project.id,
            }
        )

        self.analytic_line_2 = self.env["account.analytic.line"].create(
            {
                "name": "My Timesheet 2",
                "task_id": self.task.id,
                "unit_amount": 20,
                "project_id": self.project.id,
            }
        )

    def test_propagate_milestone_on_analytic_line(self):
        assert self.task.milestone_id & self.analytic_line_1.milestone_id

    def test_update_milestone_total_hours_when_creating_analytic_line(self):
        assert self.milestone_1.total_hours == 30

    def test_update_milestone_total_hours_when_updating_analytic_line(self):
        self.analytic_line_1.unit_amount = 20
        assert self.milestone_1.total_hours == 40

    def test_update_milestone_total_hours_when_removing_analytic_line(self):
        self.analytic_line_1.unlink()
        assert self.milestone_1.total_hours == 20

    def test_update_milestone_total_hours_when_modifying_milestone_on_task(self):
        self.task.milestone_id = self.milestone_2
        assert self.milestone_1.total_hours == 0
        assert self.milestone_2.total_hours == 30

    def test_update_milestone_total_hours_when_task_inactive(self):
        self.task.active = 0
        assert self.milestone_1.total_hours == 0
        assert self.milestone_2.total_hours == 0

    def test_update_milestone_total_hours_when_remove_project(self):
        self.milestone_1.project_id = False
        assert self.milestone_1.total_hours == 0
