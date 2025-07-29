# Copyright 2025-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    project_cost_section = fields.Selection(
        selection_add=[('supply', 'Shop Supply')],
        compute="_compute_project_cost_section",
        store=True
    )

    @api.depends(
        "is_shop_supply",
        "project_id",
        "product_id",
        "product_id.categ_id.project_cost_category_id.section",
    )
    def _compute_project_cost_section(self):
        return super(AnalyticLine, self)._compute_project_cost_section()

    def _get_project_cost_section(self):
        if self.is_shop_supply:
            return "supply"
        return super(AnalyticLine, self)._get_project_cost_section()

    def _get_project_cost_category(self):
        res = super(AnalyticLine, self)._get_project_cost_category()
        if self.project_cost_section == "supply":
            return self.env.ref("project_cost_report_supply.cost_category_supply", False)
        return res
