# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class ProjectCostReportCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Job 123"})
        cls.other_project = cls.env["project.project"].create({"name": "Job 456"})

        cls.section = "supply"

        cls.target_margin = 20
        cls.supply_category = cls.env.ref("project_cost_report.cost_category_supply")
        cls.supply_category.target_margin = cls.target_margin

        cls.time_category = cls.env.ref("project_cost_report.cost_category_labour")

        cls.analytic_account = cls.project.analytic_account_id

        cls.cost = 100
        cls.cost_line = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Cost",
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

        cls.env["account.analytic.line"].create(
            {
                "account_id": cls.other_project.analytic_account_id.id,
                "name": "Cost In Other Project",
                "is_shop_supply": True,
                "unit_amount": 1,
                "amount": 999999,
            }
        )

        cls.env["account.analytic.line"].create(
            {
                "account_id": cls.other_project.analytic_account_id.id,
                "name": "Revenue In Other Project",
                "is_shop_supply": True,
                "unit_amount": 1,
                "amount": 999999,
            }
        )

        cls.report = cls.env["project.cost.report"].create({})

    def setUp(self):
        super().setUp()
        self.report_context = {"active_id": self.project.id}

    def test_sections_order(self):
        sections = self._get_variables()["sections"]
        assert sections[0]["name"] == "supply"
        assert sections[1]["name"] == "products"
        assert sections[2]["name"] == "time"
        assert sections[3]["name"] == "outsourcing"

        assert sections[0]["title"] == "Shop Supply"
        assert sections[1]["title"] == "Products"
        assert sections[2]["title"] == "Time"
        assert sections[3]["title"] == "Outsourcing"

    def test_category_amounts(self):
        category = self._get_supply_category()
        assert category.revenue == self.revenue
        assert category.target_margin == self.target_margin
        assert category.target_sale_price == 125  # 100 / (1 - 20%)
        assert category.profit == 200  # 300 - 100
        assert category.target_profit == 25  # 125 - 100
        assert category.total_hours == 1

    def test_section_amounts(self):
        section = self._get_supply_section()
        assert section["cost"] == self.cost
        assert section["revenue"] == self.revenue
        assert section["target_sale_price"] == 125
        assert section["profit"] == 200
        assert section["target_profit"] == 25
        assert section["target_margin"] == self.target_margin
        assert section["total_hours"] == 1

    def test_total_amounts(self):
        variables = self._get_variables()
        assert variables["cost"] == self.cost
        assert variables["revenue"] == self.revenue
        assert variables["target_sale_price"] == 125
        assert variables["profit"] == 200
        assert round(variables["profit_percent"], 2) == round((200 / self.revenue) * 100, 2)
        assert variables["target_profit"] == 25
        assert variables["target_margin"] == self.target_margin
        assert variables["total_hours"] == 1

    def test_time_category_with_hourly_rate(self):
        self.cost_line.is_shop_supply = False
        self.cost_line.project_id = self.project
        self.cost_line.unit_amount = 2
        self.time_category.target_type = "hourly_rate"
        self.time_category.target_hourly_rate = 120

        category = self._get_time_category()
        assert category.target_hourly_rate == 120
        assert category.target_sale_price == 120 * 2

    def test_profit_percent_with_zero_revenue(self):
        self.revenue_line.amount = 0
        variables = self._get_variables()
        assert not variables["profit_percent"]

    def test_category_folded(self):
        assert self._get_supply_category().folded is True

    def test_category_unfolded(self):
        context = {"unfolded_categories": [self.supply_category.id]}
        assert self._get_supply_category(context).folded is False

    def test_category_cost_clicked(self):
        action = self.report.category_cost_clicked(
            self.report_context, self.section, self.supply_category.id
        )
        assert self._search_analytic_lines(action["domain"]) == self.cost_line

    def test_category_revenue_clicked(self):
        action = self.report.category_revenue_clicked(
            self.report_context, self.section, self.supply_category.id
        )
        assert self._search_analytic_lines(action["domain"]) == self.revenue_line

    def test_category_profit_clicked(self):
        action = self.report.category_profit_clicked(
            self.report_context, self.section, self.supply_category.id
        )
        assert (
            self._search_analytic_lines(action["domain"])
            == self.cost_line | self.revenue_line
        )

    def test_analytic_line_clicked(self):
        action = self.report.analytic_line_clicked(self.cost_line.id)
        assert action["res_id"] == self.cost_line.id

    def _search_analytic_lines(self, domain):
        return self.env["account.analytic.line"].search(domain)

    def _get_supply_category(self, context=None):
        return self._get_supply_section(context)["categories"][0]

    def _get_time_category(self, context=None):
        return self._get_time_section(context)["categories"][0]

    def _get_supply_section(self, context=None):
        return next(s for s in self._get_variables(context)["sections"] if s["name"] == "supply")

    def _get_time_section(self, context=None):
        return next(s for s in self._get_variables(context)["sections"] if s["name"] == "time")

    def _get_variables(self, context=None):
        return self.report.get_rendering_variables(self.project, context or {})
