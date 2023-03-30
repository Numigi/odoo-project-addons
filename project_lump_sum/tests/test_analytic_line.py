# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestAnalyticLine(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_type = cls.env["project.type"].create(
            {"name": "Lump Sum", "lump_sum": True}
        )
        cls.project = cls.env["project.project"].create(
            {"name": "Job 123", "type_id": cls.project_type.id}
        )

        cls.task = cls.env["project.task"].create(
            {"name": "Task 123", "project_id": cls.project.id}
        )

        cls.line = cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project.id,
                "name": "Line 1",
                "unit_amount": 5,
                "amount": -100,
            }
        )

    def test_is_lump_sum(self):
        assert self.line.lump_sum

    def test_not_lump_sum(self):
        self.project_type.lump_sum = False
        assert not self.line.lump_sum

    def test_is_lump_sum__origin_task(self):
        self.line.project_id = False
        self.line.origin_task_id = self.task
        assert self.line.lump_sum

    def test_not_lump_sum__origin_task(self):
        self.line.project_id = False
        self.line.origin_task_id = self.task
        self.project_type.lump_sum = False
        assert not self.line.lump_sum
