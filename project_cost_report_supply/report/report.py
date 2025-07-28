# Copyright 2025-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.tools.float_utils import float_round

SECTION_TITLES = {
    "supply": _("Shop Supply"),
    "products": _("Products"),
    "time": _("Time"),
    "outsourcing": _("Outsourcing"),
}


class ProjectCostReport(models.TransientModel):
    _inherit = "project.cost.report"

    def _get_sections(self, projects, report_context):
        return [
            self._get_section(projects, report_context, section)
            for section in ("supply", "products", "time", "outsourcing")
        ]

    def _get_section(self, projects, report_context, section_name):
        categories = self._get_section_categories(
            projects, report_context, section_name
        )
        cost = sum(c.cost for c in categories)
        revenue = sum(c.revenue for c in categories)
        profit = sum(c.profit for c in categories)
        target_sale_price = sum(c.target_sale_price for c in categories)
        target_profit = sum(c.target_profit for c in categories)
        target_margin = (
            (target_profit / target_sale_price) * 100 if target_sale_price else 0
        )
        total_hours = sum(c.total_hours for c in categories)
        return {
            "name": section_name,
            "title": _(SECTION_TITLES[section_name]),
            "categories": categories,
            "cost": float_round(cost, 2),
            "revenue": float_round(revenue, 2),
            "profit": float_round(profit, 2),
            "target_sale_price": float_round(target_sale_price, 2),
            "target_profit": float_round(target_profit, 2),
            "target_margin": float_round(target_margin, 2),
            "total_hours": float_round(total_hours, 2),
        }
