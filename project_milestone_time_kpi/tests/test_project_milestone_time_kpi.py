# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestProjectMilestoneTimeKPI(TransactionCase):
    def setUp(self):
        super().setUp()

        # create a generic Project with 2 milestones and 2 tasks associated to milestones
        self.stage = self.env["project.task.type"].create({"name": "New"})

        self.project_a = self.env["project.project"].create(
            {
                "name": "Project A",
                "allow_milestones": True,
            }
        )

        self.milestone_a = self.env["project.milestone"].create(
            {
                "name": "Analysis",
                "estimated_hours": 8,
                "project_id": self.project_a.id,
            }
        )
        self.milestone_b = self.env["project.milestone"].create(
            {
                "name": "Realization",
                "estimated_hours": 20,
                "project_id": self.project_a.id,
            }
        )

        self.task_a = self.env["project.task"].create(
            {
                "name": "Task A",
                "project_id": self.project_a.id,
                "milestone_id": self.milestone_a.id,
                "planned_hours": 4,
                "stage_id": self.stage.id,
            }
        )

        self.task_b = self.env["project.task"].create(
            {
                "name": "Task B",
                "project_id": self.project_a.id,
                "milestone_id": self.milestone_b.id,
                "planned_hours": 8,
                "stage_id": self.stage.id,
            }
        )

        # Add timelines to created tasks
        self.timesheet_a = self.env["account.analytic.line"].create(
            {
                "name": "Analyse",
                "project_id": self.project_a.id,
                "task_id": self.task_a.id,
                "unit_amount": 3,
                "employee_id": 1,
                "date": "2022-06-25",
            }
        )

        self.timesheet_b = self.env["account.analytic.line"].create(
            {
                "name": "Conception",
                "project_id": self.project_a.id,
                "task_id": self.task_b.id,
                "unit_amount": 4,
                "employee_id": 1,
                "date": "2022-06-30",
            }
        )

    def test_timesheet_line_created(self):
        """Test total_remaining_hours calculation after adding a new timeline to task"""
        self.env["account.analytic.line"].create(
            {
                "name": "Development",
                "project_id": self.project_a.id,
                "task_id": self.task_b.id,
                "unit_amount": 3,
                "employee_id": 1,
                "date": "2022-06-30",
            }
        )
        assert self.project_a.total_estimated_hours == 28
        assert self.project_a.total_spent_hours == 10
        assert self.project_a.total_remaining_hours == 2

    def test_add_milestone(self):
        self.env["project.milestone"].create(
            {
                "name": "Test",
                "estimated_hours": 8,
                "project_id": self.project_a.id,
            }
        )
        assert self.project_a.total_estimated_hours == 36

    def test_unlink_milestone(self):
        self.milestone_b.unlink()
        assert self.project_a.total_estimated_hours == 8
        assert self.project_a.total_spent_hours == 3

    def test_update_milestone(self):
        self.milestone_a.write({"estimated_hours": 10})
        assert self.project_a.total_estimated_hours == 30
