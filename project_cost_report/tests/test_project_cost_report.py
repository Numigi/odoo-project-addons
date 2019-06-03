# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from ..report import CostReportCategory


class TestProjectCostReport(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
        })

        cls.analytic_account = cls.project.analytic_account_id

        cls.category_a = cls.env['product.category'].create({
            'name': 'Category A',
        })

        cls.category_b = cls.env['product.category'].create({
            'name': 'Category B',
        })

        cls.product_a = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'categ_id': cls.category_a.id,
        })

        cls.product_b = cls.env['product.product'].create({
            'name': 'Product B',
            'type': 'product',
            'categ_id': cls.category_b.id,
        })

        cls.line_1 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 1',
            'product_id': cls.product_a.id,
            'quantity': 1,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': 100,
        })

        cls.line_2 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 1',
            'product_id': cls.product_b.id,
            'quantity': 2,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': 200,
        })

        cls.line_3 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 1',
            'product_id': cls.product_b.id,
            'quantity': 3,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': 300,
        })

        cls.report = cls.env['project.cost.report'].create({})

    def _get_product_categories(self, report_context=None):
        return self.report._get_product_categories(self.project, report_context or {})

    def test_all_product_categories_found_in_report(self):
        categories = self._get_product_categories()
        assert len(categories) == 2
        assert isinstance(categories[0], CostReportCategory)
        assert isinstance(categories[1], CostReportCategory)

    def test_all_product_analytic_lines_found_in_categories(self):
        categories = self._get_product_categories()

        assert len(categories[0].lines) == 1
        assert self.line_1 in categories[0].lines

        assert len(categories[1].lines) == 2
        assert self.line_2 in categories[1].lines
        assert self.line_3 in categories[1].lines

    def test_product_analytic_lines_include_consummable(self):
        self.product_a.type = 'consu'
        categories = self._get_product_categories()
        assert self.line_1 in categories[0].lines

    def test_product_analytic_lines_not_include_services(self):
        self.product_a.type = 'service'
        categories = self._get_product_categories()
        assert self.line_1 not in categories[0].lines

    def test_product_category_name_is_set(self):
        categories = self._get_product_categories()
        assert categories[0].name == self.category_a.name
        assert categories[1].name == self.category_b.name

    def test_if_no_unfolded_category_given__then_all_categories_folded(self):
        categories = self._get_product_categories()
        assert categories[0].folded is True
        assert categories[1].folded is True

    def test_if_single_folded_category_id__then_single_categories_folded(self):
        categories = self._get_product_categories({'unfolded_category_ids': [self.category_a.id]})
        assert categories[0].folded is False
        assert categories[1].folded is True

    def test_product_total_is_sum_of_all_product_amounts(self):
        total = self.report._get_product_total(self.project)
        assert total == 600  # 100 + 200 + 300 (sum of line_1, line_2 and line_3)

    def test_category_total_is_sum_of_analytic_lines(self):
        categories = self._get_product_categories({'unfolded_category_ids': [self.category_a.id]})
        assert categories[0].total == 100
        assert categories[1].total == 500
