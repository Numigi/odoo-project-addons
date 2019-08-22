# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_cost_report.tests.test_project_cost_report import ProjectCostReportCase
from odoo.addons.project_cost_report.report import CostReportCategory


class TestProjectCostReportWithShopSupply(ProjectCostReportCase):
    """Test the report with shop supply entries.

    The test class is inherited directly to make sure this module does not break existing sections
    unrelated to shop supply.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.shop_supply_line_1 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Shop Supply 1',
            'product_uom_id': cls.env.ref('product.product_uom_hour').id,
            'unit_amount': 10,
            'amount': -1000,
            'is_shop_supply': True,
        })

        cls.shop_supply_line_2 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Shop Supply 2',
            'product_uom_id': cls.env.ref('product.product_uom_hour').id,
            'unit_amount': 11,
            'amount': -1100,
            'is_shop_supply': True,
        })

    def _get_shop_supply_categories(self, report_context=None):
        return self.report._get_shop_supply_categories(self.project, report_context or {})

    def test_empty_shop_supply_categories_found_in_report(self):
        categories = self._get_shop_supply_categories()
        assert len(categories) == 1
        assert isinstance(categories[0], CostReportCategory)

    def test_if_no_shop_supply_analytic_lines__then_no_categories(self):
        self.shop_supply_line_1.unlink()
        self.shop_supply_line_2.unlink()
        categories = self._get_shop_supply_categories()
        assert len(categories) == 0

    def test_empty_shop_supply_category_id_is_false(self):
        categories = self._get_shop_supply_categories()
        assert categories[0].id is False

    def test_all_shop_supply_analytic_lines_found_in_categories(self):
        categories = self._get_shop_supply_categories()

        assert len(categories[0].lines) == 2
        assert self.shop_supply_line_1 in categories[0].lines
        assert self.shop_supply_line_2 in categories[0].lines

    def test_if_no_unfolded_category_given__then_all_shop_supply_categories_folded(self):
        categories = self._get_shop_supply_categories()
        assert categories[0].folded is True

    def test_if_false_in_folded_shop_supply_categories__then_empty_category_unfolded(self):
        categories = self._get_shop_supply_categories({
            'unfolded_categories': {
                'shop_supply': [False],
            }
        })
        assert categories[0].folded is False

    def test_shop_supply_total_is_sum_of_all_shop_supply_amounts(self):
        total = self.report._get_shop_supply_total(self.project)
        # 1000 + 1100 (sum of shop_supply_line_1 and shop_supply_line_2)
        assert total == 2100
