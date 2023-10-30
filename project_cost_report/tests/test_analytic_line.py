# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestAnalyticLine(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_cost_category = cls.env.ref(
            "project_cost_report.cost_category_product"
        )
        cls.labour_cost_category = cls.env.ref(
            "project_cost_report.cost_category_labour"
        )
        cls.outsourcing_cost_category = cls.env.ref(
            "project_cost_report.cost_category_outsourcing"
        )
        cls.supply_cost_category = cls.env.ref(
            "project_cost_report.cost_category_supply"
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

    def test_if_unit_amount_not_null__unit_cost_is_computed(self):
        assert self.line.unit_cost == 20  # -(-100 / 5)

    def test_if_unit_amount_is_null__unit_cost_is_zero(self):
        self.line.unit_amount = 0
        assert self.line.unit_cost == 0

    def test_cost_section__time(self):
        self.line.project_id = self.project
        assert self.line.project_cost_section == "time"
        assert self.line.project_cost_category_id == self.labour_cost_category

    def test_cost_section__from_task_type(self):
        self.line.project_id = self.project
        self.line.task_id = self.task
        assert self.line.project_cost_section == "time"
        assert self.line.project_cost_category_id == self.custom_time_category

    def test_cost_section__products(self):
        self.line.product_id = self.product
        self.product.categ_id.project_cost_category_id = self.product_cost_category
        assert self.line.project_cost_section == "products"
        assert self.line.project_cost_category_id == self.product_cost_category

    def test_cost_section__time_category(self):
        self.line.product_id = self.product
        self.product.categ_id.project_cost_category_id = self.labour_cost_category
        assert self.line.project_cost_section == "time"
        assert self.line.project_cost_category_id == self.labour_cost_category

    def test_cost_section__outsourcing(self):
        self.line.product_id = self.product
        self.product.categ_id.project_cost_category_id = self.outsourcing_cost_category
        assert self.line.project_cost_section == "outsourcing"
        assert self.line.project_cost_category_id == self.outsourcing_cost_category

    def test_cost_section__supply(self):
        self.line.is_shop_supply = True
        assert self.line.project_cost_section == "supply"
        assert self.line.project_cost_category_id == self.supply_cost_category
