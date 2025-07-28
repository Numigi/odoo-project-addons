# Copyright 2019-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class ProjectCostReportCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Job 123"})
        cls.cost = 100
        cls.section = "supply"
        cls.target_margin = 20
        cls.supply_category = cls.env.ref("project_cost_report_supply.cost_category_supply")
        cls.supply_category.target_margin = cls.target_margin
        cls.analytic_account = cls.project.analytic_account_id
        cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account,
                "name": "Cost In Other Project",
                "is_shop_supply": True,
                "unit_amount": 1,
                "amount": -cls.cost,
            }
        )
        cls.revenue = 300
        cls.revenue_line = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                 "name": "Revenue",
                 "is_shop_supply": True,
                "revenue": True,
                 "unit_amount": 1,
                 "amount": cls.revenue,
             }
        )

        cls.report = cls.env["project.cost.report"].create({})

    def setUp(self):
        super().setUp()
        self.report_context = {"active_id": self.project.id}

    def test_section_amounts(self):
        section = self._get_supply_section()
        print("99999999999999999",section)
        assert section["cost"] == self.cost
        assert section["revenue"] == self.revenue
        assert section["target_sale_price"] == 125
        assert section["profit"] == 200
        assert section["target_profit"] == 25
        assert section["target_margin"] == self.target_margin
        assert section["total_hours"] == 1


    def _get_supply_category(self, context=None):
        return self._get_supply_section(context)["categories"][0]

    def _get_supply_section(self, context=None):
        return next(
            s for s in self._get_variables(context)["sections"] if s["name"] == "supply"
        )
    def _get_variables(self, context=None):
        return self.report.get_rendering_variables(self.project, context or {})



