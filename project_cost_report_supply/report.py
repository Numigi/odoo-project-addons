# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.osv.expression import AND
from odoo.tools.float_utils import float_round
from odoo.addons.project_cost_report.report.util import CostReportCategory


def is_shop_supply_line(analytic_line):
    return analytic_line.is_shop_supply


class ProjectCostReportWithShopSupply(models.TransientModel):

    _inherit = "project.cost.report"

    def get_rendering_variables(self, project, report_context):
        """Add the variables related to the OUTSOURCING section."""
        res = super().get_rendering_variables(project, report_context)

        shop_supply_total = self._get_shop_supply_total(project)
        shop_supply_categories = self._get_shop_supply_categories(
            project, report_context
        )
        shop_supply_sale_price = self._get_total_section_sale_price(
            shop_supply_categories
        )

        total_cost = float_round(res["total_cost"] + shop_supply_total, 2)
        total_sale_price = float_round(
            res["total_target_sale_price"] + shop_supply_sale_price, 2
        )
        total_profit = total_sale_price - total_cost
        total_margin = (
            (total_profit / total_sale_price) * 100 if total_sale_price else 0
        )

        res.update(
            {
                "is_shop_supply_line": is_shop_supply_line,
                "shop_supply_categories": shop_supply_categories,
                "shop_supply_total": shop_supply_total,
                "total_cost": float_round(total_cost, 2),
                "total_profit": float_round(total_profit, 2),
                "total_target_margin": float_round(total_margin, 2),
                "total_target_sale_price": float_round(total_sale_price, 2),
            }
        )
        return res

    def _get_shop_supply_categories(self, project, report_context):
        """Get the SHOP SUPPLY sections.

        Outsourcing has only one category (False).
        """
        unfolded_categories = report_context.get("unfolded_categories") or {}
        unfolded_shop_supply_categories = unfolded_categories.get("shop_supply") or []
        result = []
        lines = self._get_shop_supply_analytic_lines(project)
        supply_category = self.env.ref(
            "project_cost_report_supply.cost_category_supply"
        )
        if lines:
            empty_category = CostReportCategory(
                supply_category,
                lines=lines,
                folded=supply_category.id not in unfolded_shop_supply_categories,
            )
            result.append(empty_category)
        return result

    def _get_shop_supply_total(self, project):
        lines = self._get_shop_supply_analytic_lines(project)
        total_amount = sum(l.amount for l in lines)
        return float_round(-total_amount, 2)

    def _get_shop_supply_analytic_lines(self, project):
        return project.analytic_account_id.line_ids.filtered(
            lambda l: is_shop_supply_line(l)
        )

    def _get_product_analytic_lines(self, project):
        lines = super()._get_product_analytic_lines(project)
        return lines.filtered(lambda l: not is_shop_supply_line(l))

    def _get_timesheet_analytic_lines(self, project):
        lines = super()._get_timesheet_analytic_lines(project)
        return lines.filtered(lambda l: not is_shop_supply_line(l))

    def _get_outsourcing_analytic_lines(self, project):
        lines = super()._get_outsourcing_analytic_lines(project)
        return lines.filtered(lambda l: not is_shop_supply_line(l))
