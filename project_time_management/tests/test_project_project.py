# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from ddt import data, ddt, unpack


@ddt
class TestProjectWithCalculatedHoursFields(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env["project.project"].create({"name": "Project A"})
        analytic_line_pool = cls.env["account.analytic.line"]
        task_pool = cls.env["project.task"]

        task_a = task_pool.create(
            {
                "name": "task_a",
                "min_hours": 1.0,
                "max_hours": 4.0,
                "planned_hours": 3.0,
                "project_id": cls.project_a.id,
            }
        )
        analytic_line_pool.create(
            {
                "name": "line_task_a",
                "unit_amount": 1.0,
                "task_id": task_a.id,
                "project_id": cls.project_a.id,
            }
        )

        cls.project_b = cls.env["project.project"].create({"name": "Project B"})
        task_b1 = task_pool.create(
            {
                "name": "task_b1",
                "min_hours": 1.0,
                "max_hours": 4.0,
                "planned_hours": 3.0,
                "project_id": cls.project_b.id,
            }
        )
        analytic_line_pool.create(
            {
                "name": "line_task_b1",
                "unit_amount": 1.0,
                "task_id": task_b1.id,
                "project_id": cls.project_b.id,
            }
        )
        task_b2 = task_pool.create(
            {
                "name": "task_b2",
                "min_hours": 2.0,
                "max_hours": 8.0,
                "planned_hours": 6.0,
                "project_id": cls.project_b.id,
            }
        )
        analytic_line_pool.create(
            {
                "name": "line_task_b2",
                "unit_amount": 6.0,
                "task_id": task_b2.id,
                "project_id": cls.project_b.id,
            }
        )
        # as it is a subtask, should be out of the scope
        task_pool.create(
            {
                "name": "task_b3",
                "parent_id": task_b2.id,
                "min_hours": 2.0,
                "max_hours": 8.0,
                "planned_hours": 6.0,
                "project_id": cls.project_b.id,
            }
        )

    @data(
        ["calculated_min_hours", 1.0],
        ["calculated_max_hours", 4.0],
        ["calculated_planned_hours", 3.0],
        ["calculated_remaining_hours", 2.0],
        ["calculated_total_hours_spent", 1.0],
    )
    @unpack
    def test_caseOfSingleTask(self, field, expected_value):
        """ Project with a single task assigned to it."""
        assert expected_value == self.project_a.__getattribute__(field)

    @data(
        ["calculated_min_hours", 3.0],
        ["calculated_max_hours", 12.0],
        ["calculated_planned_hours", 9.0],
        ["calculated_remaining_hours", 2.0],
        ["calculated_total_hours_spent", 7.0],
    )
    @unpack
    def test_caseMultipleTasks(self, field, expected_value):
        """ Project with several tasks assigned to it, with a sub task."""
        assert expected_value == self.project_b.__getattribute__(field)
