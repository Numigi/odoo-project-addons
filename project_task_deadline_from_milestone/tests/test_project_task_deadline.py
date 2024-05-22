# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo.tests import common


class TestProjectTaskDeadline(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.deadline = date(2018, 3, 1)
        cls.project_with_deadline = cls.env["project.project"].create(
            {
                "name": "Project With Deadline",
                "date": cls.deadline,
            }
        )
        cls.task = cls.env["project.task"].create({"name": "My Task Test"})
        cls.test_project_milestone = cls.env["project.milestone"].create(
            {
                "name": "TestMilestone",
                "project_id": cls.project_with_deadline.id,
                "target_date": date(2024, 6, 1),
            }
        )

    def test_01_create_task_with_milestone(self):
        """Create project task with milestone"""
        task = self._create_task(
            self.project_with_deadline, self.test_project_milestone.id
        )
        self.assertEqual(task.date_deadline, self.test_project_milestone.target_date)

    def test_02_create_task__no_milestone_with_project__then_add_milestone(self):
        """Create project task without milestone, then add milestone"""
        task = self._create_task(self.project_with_deadline)
        self.assertEqual(task.date_deadline, self.project_with_deadline.date)
        # Add milestone and check if task deadline is set to milestone target_date
        task.milestone_id = self.test_project_milestone.id
        task._onchange_project_propagate_deadline()
        self.assertEqual(task.date_deadline, self.test_project_milestone.target_date)
        # Then try to remove milestone and restore task deadline to project date automatically
        task.milestone_id = False
        task._onchange_project_propagate_deadline()
        self.assertEqual(task.date_deadline, self.project_with_deadline.date)

    def test_03_create_task_without_milestone(self):
        """Create project task without milestone"""
        task = self._create_task(self.project_with_deadline)
        self.assertEqual(task.date_deadline, self.project_with_deadline.date)

    def _create_task(self, project, milestone=False):
        return self.env["project.task"].create(
            {
                "name": "Task with milestone",
                "milestone_id": milestone,
                "project_id": project.id,
            }
        )
