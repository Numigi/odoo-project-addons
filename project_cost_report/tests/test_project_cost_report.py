# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from ..report import CostReportCategory


class ProjectCostReportCase(common.SavepointCase):

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

        cls.service_a = cls.env['product.product'].create({
            'name': 'Service A',
            'type': 'service',
            'categ_id': cls.category_a.id,
        })

        cls.product_line_1 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 1',
            'product_id': cls.product_a.id,
            'unit_amount': 1,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': -100,
        })

        cls.product_line_2 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 2',
            'product_id': cls.product_b.id,
            'unit_amount': 2,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': -200,
        })

        cls.product_line_3 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 3',
            'product_id': cls.product_b.id,
            'unit_amount': 3,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': -300,
        })

        cls.task_type_1 = cls.env['task.type'].create({'name': 'Type 1'})
        cls.task_type_2 = cls.env['task.type'].create({'name': 'Type 2'})

        cls.task_1 = cls.env['project.task'].create({
            'name': 'Task 1',
            'project_id': cls.project.id,
        })

        cls.task_2 = cls.env['project.task'].create({
            'name': 'Task 2',
            'project_id': cls.project.id,
            'task_type_id': cls.task_type_1.id,
        })

        cls.task_3 = cls.env['project.task'].create({
            'name': 'Task 3',
            'project_id': cls.project.id,
            'task_type_id': cls.task_type_2.id,
        })

        cls.env.user.employee_ids.write({'timesheet_cost': 100})

        cls.time_line_1 = cls.env['account.analytic.line'].create({
            'project_id': cls.project.id,
            'name': 'Time 1',
            'product_uom_id': cls.env.ref('product.product_uom_hour').id,
            'unit_amount': 4,
            'amount': -400,
            'user_id': cls.env.user.id,
            'task_id': cls.task_1.id,
        })

        cls.time_line_2 = cls.env['account.analytic.line'].create({
            'project_id': cls.project.id,
            'name': 'Time 2',
            'product_uom_id': cls.env.ref('product.product_uom_hour').id,
            'unit_amount': 5,
            'amount': -500,
            'user_id': cls.env.user.id,
            'task_id': cls.task_2.id,
        })

        cls.time_line_3 = cls.env['account.analytic.line'].create({
            'project_id': cls.project.id,
            'name': 'Time 3',
            'product_uom_id': cls.env.ref('product.product_uom_hour').id,
            'unit_amount': 6,
            'amount': -600,
            'user_id': cls.env.user.id,
            'task_id': cls.task_2.id,
        })

        cls.time_line_4 = cls.env['account.analytic.line'].create({
            'project_id': cls.project.id,
            'name': 'Time 3',
            'product_uom_id': cls.env.ref('product.product_uom_hour').id,
            'unit_amount': 7,
            'amount': -700,
            'user_id': cls.env.user.id,
            'task_id': cls.task_3.id,
        })

        cls.outsourcing_line_1 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Service Line 1',
            'product_id': cls.service_a.id,
            'unit_amount': 1,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': -800,
        })

        cls.outsourcing_line_2 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Service Line 2',
            'product_id': cls.service_a.id,
            'unit_amount': 2,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': -900,
        })

        # Add revenue analytic lines
        # These amounts must be excluded from cost categories
        # (Outsourcing, Products, Time)
        cls.revenue_line_1 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Revenue Line 1',
            'product_id': cls.service_a.id,
            'unit_amount': 1,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': 100,
            'revenue': True,
        })

        cls.revenue_line_2 = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Revenue Line 2',
            'product_id': cls.product_a.id,
            'unit_amount': 1,
            'product_uom_id': cls.env.ref('product.product_uom_unit').id,
            'amount': 200,
            'revenue': True,
        })

        cls.report = cls.env['project.cost.report'].create({})


class TestProjectCostReport(ProjectCostReportCase):

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
        assert self.product_line_1 in categories[0].lines

        assert len(categories[1].lines) == 2
        assert self.product_line_2 in categories[1].lines
        assert self.product_line_3 in categories[1].lines

    def test_product_analytic_lines_include_consummable(self):
        self.product_a.type = 'consu'
        categories = self._get_product_categories()
        assert self.product_line_1 in categories[0].lines

    def test_product_analytic_lines_not_include_services(self):
        self.product_a.type = 'service'
        categories = self._get_product_categories()
        assert self.product_line_1 not in categories[0].lines

    def test_product_category_name_is_set(self):
        categories = self._get_product_categories()
        assert categories[0].name == self.category_a.name
        assert categories[1].name == self.category_b.name

    def test_if_no_unfolded_category_given__then_all_categories_folded(self):
        categories = self._get_product_categories()
        assert categories[0].folded is True
        assert categories[1].folded is True

    def test_if_single_folded_category_id__then_single_categories_folded(self):
        categories = self._get_product_categories({
            'unfolded_categories': {
                'product': [self.category_a.id],
            }
        })
        assert categories[0].folded is False
        assert categories[1].folded is True

    def test_product_total_is_sum_of_all_product_amounts(self):
        total = self.report._get_product_total(self.project)
        # 100 + 200 + 300 (sum of product_line_1, product_line_2 and product_line_3)
        assert total == 600

    def test_category_total_is_sum_of_analytic_lines(self):
        categories = self._get_product_categories()
        assert categories[0].total == 100
        assert categories[1].total == 500

    def _get_time_categories(self, report_context=None):
        return self.report._get_time_categories(self.project, report_context or {})

    def test_all_time_categories_found_in_report(self):
        categories = self._get_time_categories()
        assert len(categories) == 3
        assert isinstance(categories[0], CostReportCategory)
        assert isinstance(categories[1], CostReportCategory)
        assert isinstance(categories[2], CostReportCategory)

    def test_all_time_analytic_lines_found_in_categories(self):
        categories = self._get_time_categories()

        assert len(categories[0].lines) == 1
        assert self.time_line_1 in categories[0].lines

        assert len(categories[1].lines) == 2
        assert self.time_line_2 in categories[1].lines
        assert self.time_line_3 in categories[1].lines

        assert len(categories[2].lines) == 1
        assert self.time_line_4 in categories[2].lines

    def test_time_category_name_is_task_type_name(self):
        categories = self._get_time_categories()
        assert categories[1].name == self.task_type_1.name
        assert categories[2].name == self.task_type_2.name

    def test_if_no_unfolded_category_given__then_all_time_categories_folded(self):
        categories = self._get_time_categories()
        assert categories[0].folded is True
        assert categories[1].folded is True
        assert categories[2].folded is True

    def test_if_folded_task_type_id__then_single_time_category_folded(self):
        categories = self._get_time_categories({
            'unfolded_categories': {
                'time': [self.task_type_1.id],
            }
        })
        assert categories[0].folded is True
        assert categories[1].folded is False
        assert categories[2].folded is True

    def test_if_false_in_folded_time_categories__then_empty_category_unfolded(self):
        categories = self._get_time_categories({
            'unfolded_categories': {
                'time': [False],
            }
        })
        assert categories[0].folded is False
        assert categories[1].folded is True
        assert categories[2].folded is True

    def test_time_total_is_sum_of_all_time_amounts(self):
        total = self.report._get_time_total(self.project)
        # 400 + 500 + 600 + 700 (sum of time_line_1, time_line_2 and time_line_3, time_line_4)
        assert total == 2200

    def test_time_total_hours_is_sum_of_all_time_amounts(self):
        total = self.report._get_time_total_hours(self.project)
        # 4 + 5 + 6 + 7 (sum of time_line_1, time_line_2 and time_line_3, time_line_4)
        assert total == 22

    def test_get_html_returns_bytestring(self):
        html = self.report.get_html({'active_id': self.project.id})
        assert isinstance(html, bytes)

    def _get_outsourcing_categories(self, report_context=None):
        return self.report._get_outsourcing_categories(self.project, report_context or {})

    def test_empty_outsourcing_categories_found_in_report(self):
        categories = self._get_outsourcing_categories()
        assert len(categories) == 1
        assert isinstance(categories[0], CostReportCategory)

    def test_if_no_outsourcing_analytic_lines__then_no_categories(self):
        self.outsourcing_line_1.unlink()
        self.outsourcing_line_2.unlink()
        categories = self._get_outsourcing_categories()
        assert len(categories) == 0

    def test_empty_outsourcing_category_id_is_false(self):
        categories = self._get_outsourcing_categories()
        assert categories[0].id is False

    def test_all_outsourcing_analytic_lines_found_in_categories(self):
        categories = self._get_outsourcing_categories()

        assert len(categories[0].lines) == 2
        assert self.outsourcing_line_1 in categories[0].lines
        assert self.outsourcing_line_2 in categories[0].lines

    def test_if_no_unfolded_category_given__then_all_outsourcing_categories_folded(self):
        categories = self._get_outsourcing_categories()
        assert categories[0].folded is True

    def test_if_false_in_folded_outsourcing_categories__then_empty_category_unfolded(self):
        categories = self._get_outsourcing_categories({
            'unfolded_categories': {
                'outsourcing': [False],
            }
        })
        assert categories[0].folded is False

    def test_outsourcing_total_is_sum_of_all_outsourcing_amounts(self):
        total = self.report._get_outsourcing_total(self.project)
        # 800 + 900 (sum of outsourcing_line_1 and outsourcing_line_2)
        assert total == 1700
