# Copyright 2025-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestAnalyticLine(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.supply_cost_category = cls.env.ref(
            "project_cost_report_supply.cost_category_supply"
        )

        cls.product = cls.env["product.product"].create({"name": "My Product"})

        cls.project = cls.env["project.project"].create({"name": "Job 123"})

        cls.custom_time_category = cls.env["project.cost.category"].create(
            {"name": "Custom Time Category"}
        )
        cls.task_type = cls.env["task.type"].create(
            {
                "name": "Task Type",
                "project_cost_category_id": cls.custom_time_category.id,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Task",
                "project_id": cls.project.id,
                "task_type_id": cls.task_type.id,
            }
        )

        cls.analytic_account = cls.project.analytic_account_id

        cls.line = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Line 1",
                "unit_amount": 5,
                "amount": -100,
            }
        )


    def test_cost_section__supply(self):
        self.line.is_shop_supply = True
        assert self.line.project_cost_section == "supply"
        assert self.line.project_cost_category_id == self.supply_cost_category
