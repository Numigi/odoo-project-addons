# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import ProjectCostReportCase


class TestProjectCostReport(ProjectCostReportCase):
    def _get_product_categories(self, report_context=None):
        return self.report._get_product_categories(self.project, report_context or {})

    def test_all_product_categories_found_in_report(self):
        categories = self._get_product_categories()
        assert len(categories) == 2

    def test_all_product_analytic_lines_found_in_categories(self):
        categories = self._get_product_categories()

        assert len(categories[0].lines) == 1
        assert self.product_line_1 in categories[0].lines

        assert len(categories[1].lines) == 2
        assert self.product_line_2 in categories[1].lines
        assert self.product_line_3 in categories[1].lines

    def test_product_analytic_lines_include_consummable(self):
        self.product_a.type = "consu"
        categories = self._get_product_categories()
        assert self.product_line_1 in categories[0].lines

    def test_product_analytic_lines_not_include_services(self):
        self.product_a.type = "service"
        categories = self._get_product_categories()
        assert self.product_line_1 not in categories[0].lines

    def test_product_category_name_is_set(self):
        categories = self._get_product_categories()
        assert categories[0].name == self.product_group_a.name
        assert categories[1].name == self.product_group_b.name

    def test_if_no_unfolded_category_given__then_all_categories_folded(self):
        categories = self._get_product_categories()
        assert categories[0].folded is True
        assert categories[1].folded is True

    def test_if_single_folded_category_id__then_single_categories_folded(self):
        categories = self._get_product_categories(
            {"unfolded_categories": {"product": [self.product_group_a.id]}}
        )
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
        assert categories[0].name == self.time_group_labour.name
        assert categories[1].name == self.time_group_1.name
        assert categories[2].name == self.time_group_2.name

    def test_if_no_unfolded_category_given__then_all_time_categories_folded(self):
        categories = self._get_time_categories()
        assert categories[0].folded is True
        assert categories[1].folded is True
        assert categories[2].folded is True

    def test_if_folded_task_type_id__then_single_time_category_folded(self):
        categories = self._get_time_categories(
            {
                "unfolded_categories": {
                    "time": [self.time_group_1.id, self.time_group_labour.id]
                }
            }
        )
        assert categories[0].folded is False
        assert categories[1].folded is False
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
        html = self.report.get_html({"active_id": self.project.id})
        assert isinstance(html, bytes)

    def _get_outsourcing_categories(self, report_context=None):
        return self.report._get_outsourcing_categories(
            self.project, report_context or {}
        )

    def test_empty_outsourcing_categories_found_in_report(self):
        categories = self._get_outsourcing_categories()
        assert len(categories) == 1

    def test_if_no_outsourcing_analytic_lines__then_no_categories(self):
        self.outsourcing_line_1.unlink()
        self.outsourcing_line_2.unlink()
        categories = self._get_outsourcing_categories()
        assert len(categories) == 0

    def test_all_outsourcing_analytic_lines_found_in_categories(self):
        categories = self._get_outsourcing_categories()

        assert len(categories[0].lines) == 2
        assert self.outsourcing_line_1 in categories[0].lines
        assert self.outsourcing_line_2 in categories[0].lines

    def test_if_no_unfolded_category_given__then_all_outsourcing_categories_folded(
        self,
    ):
        categories = self._get_outsourcing_categories()
        assert categories[0].folded is True

    def test_if_false_in_folded_outsourcing_categories__then_empty_category_unfolded(
        self,
    ):
        categories = self._get_outsourcing_categories(
            {"unfolded_categories": {"outsourcing": [self.outsourcing_group.id]}}
        )
        assert categories[0].folded is False

    def test_outsourcing_total_is_sum_of_all_outsourcing_amounts(self):
        total = self.report._get_outsourcing_total(self.project)
        # 800 + 900 (sum of outsourcing_line_1 and outsourcing_line_2)
        assert total == 1700

    def test_product_target_margin(self):

        categories = self._get_product_categories()
        assert categories[0].target_sale_price == 156.25  # 100 / (1 - 36%)
        assert categories[1].target_sale_price == 1000  # 500 / (1 - 50%)
        assert categories[0].target_profit == 56.25  # 156.25 - 100
        assert categories[1].target_profit == 500  # 1000 - 500

    def test_time_target_margin(self):

        categories = self._get_time_categories()
        assert categories[0].target_sale_price == 400  # 4 * 100
        assert categories[1].target_sale_price == 2200  # 11 * 200
        assert categories[2].target_sale_price == 2100  # 7 * 300
        assert categories[0].target_profit == 0  # 400 - 400
        assert categories[1].target_profit == 1100  # 2200 - 1100
        assert categories[2].target_profit == 1400  # 2100 - 700

    def test_outsourcing_target_margin(self):
        categories = self._get_outsourcing_categories()
        assert categories[0].target_sale_price == 2125  # 1700 / (1 - 0.2)
        assert categories[0].target_profit == 425  # 2125 - 1700

    def test_global_target_margin(self):
        variables = self.report.get_rendering_variables(self.project, {})
        assert (
            variables["total_cost"] == 4500
        )  # 600 + 2200 + 1700 (products + time + outsourcing)
        # 156.25 + 1000 + 400 + 2200 + 2100 + 2125
        assert variables["total_target_sale_price"] == 7981.25
        assert variables["total_profit"] == 3481.25  # 56.25 + 500 + 1100 + 1400 + 425
        assert variables["total_target_margin"] == round((3481.25 / 7981.25) * 100, 2)
