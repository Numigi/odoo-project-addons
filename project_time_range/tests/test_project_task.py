# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data, unpack
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestTasks(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_a = (
            cls.env["project.task"]
            .with_context(enable_task_max_hours_constraint=True)
            .create({"name": "Task A"})
        )

    def test_defaulValues(self):
        self.task_a.write({"min_hours": 0, "planned_hours": 0, "max_hours": 0})

    def test_whenIdealDifferent0_thenMinHasToBeLesserThanIdeal(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({"planned_hours": 10, "min_hours": 11})

    def test_whenIdealDifferent0_theMinCanBeEqualToIdeal(self):
        self.task_a.write({"planned_hours": 10, "min_hours": 10, "max_hours": 11})
        assert self.task_a.min_hours == 10

    def test_whenIdealDifferent0_thenMaxHasToBeGreaterThanIdeal(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({"planned_hours": 10, "max_hours": 9})

    def test_whenIdealDifferent0_theMaxCanBeEqualToIdeal(self):
        self.task_a.write({"planned_hours": 10, "max_hours": 10})
        assert self.task_a.max_hours == 10

    def test_idealCanBeNone(self):
        self.task_a.write({"planned_hours": None})
        assert self.task_a.max_hours == 0
        assert self.task_a.min_hours == 0

    def test_whenIdealIsZero_thenConstrainsAreStillApplied(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({"min_hours": 4, "planned_hours": 0, "max_hours": 2})

    def test_negativeNumbersAreNotAllowed(self):
        with self.assertRaises(ValidationError):
            self.task_a.write({"min_hours": -10, "planned_hours": -2, "max_hours": 0})


@ddt
class TestSubtasks(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_no_child = cls.env["project.task"].create({"name": "Task No Child"})
        cls.task_parent = cls.env["project.task"].create({"name": "Task Parent"})

        cls.task_child1 = cls.env["project.task"].create(
            {
                "name": "Task Child 1",
                "parent_id": cls.task_parent.id,
                "min_hours": 0.5,
                "planned_hours": 1.0,
                "max_hours": 2.0,
            }
        )
        cls.task_child2 = cls.env["project.task"].create(
            {
                "name": "Task Child 2",
                "parent_id": cls.task_parent.id,
                "min_hours": 0.5,
                "planned_hours": 1.0,
                "max_hours": 2.0,
            }
        )
        cls.task_child3 = cls.env["project.task"].create(
            {
                "name": "Task Child 3",
                "parent_id": cls.task_parent.id,
                "min_hours": 5,
                "planned_hours": 10,
                "max_hours": 20.0,
            }
        )

        cls.task_child4 = cls.env["project.task"].create(
            {
                "name": "Task Child 4",
                "min_hours": 0.5,
                "planned_hours": 1.0,
                "max_hours": 2.0,
            }
        )

    @data("subtask_min_hours", "subtask_max_hours", "subtask_planned_hours")
    def test_whenTaskWithNoChild_thenComputedFieldsReturn0(self, field):
        assert 0 == self.task_no_child[field]

    @data(
        ["subtask_min_hours", 6],
        ["subtask_planned_hours", 12.0],
        ["subtask_max_hours", 24.0],
    )
    @unpack
    def test_whenTaskWithChild_thenComputedFieldsReturnSumOfChildValues(
        self, field, expected_value
    ):
        assert expected_value == self.task_parent[field]
