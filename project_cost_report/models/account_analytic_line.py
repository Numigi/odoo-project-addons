# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    unit_cost = fields.Monetary(compute="_compute_unit_cost")
    project_cost_section = fields.Selection(
        [
            ("products", "Products"),
            ("time", "Time"),
            ("outsourcing", "Outsourcing"),
        ],
        compute="_compute_project_cost_section",
        store=True,
    )
    project_cost_category_id = fields.Many2one(
        "project.cost.category", compute="_compute_project_cost_category", store=True
    )

    @api.depends("amount", "unit_amount")
    def _compute_unit_cost(self):
        for line in self:
            sign = 1 if line.revenue else -1
            line.unit_cost = sign * (
                line.amount / line.unit_amount if line.unit_amount else 0
            )

    @api.depends(
        "project_id",
        "product_id",
        "product_id.categ_id.project_cost_category_id.section",
    )
    def _compute_project_cost_section(self):
        for line in self:
            line.project_cost_section = line._get_project_cost_section()

    def _get_project_cost_section(self):
        if self.project_id or not self.product_id:
            return "time"

        return self.product_id.categ_id.project_cost_category_id.section

    @api.depends(
        "project_cost_section",
        "product_id.categ_id.project_cost_category_id",
        "task_id.task_type_id.project_cost_category_id",
    )
    def _compute_project_cost_category(self):
        for line in self:
            line.project_cost_category_id = line._get_project_cost_category()

    def _get_project_cost_category(self):
        category = self.product_id.categ_id.project_cost_category_id
        if category:
            return category

        if self.project_cost_section == "time":
            return self._get_time_cost_category()

        if self.project_cost_section == "products":
            return self.env.ref("project_cost_report.cost_category_product", False)

        if self.project_cost_section == "outsourcing":
            return self.env.ref("project_cost_report.cost_category_outsourcing", False)

    def _get_time_cost_category(self):
        time_category = self.task_id.task_type_id.project_cost_category_id
        if time_category:
            return time_category

        return self.env.ref("project_cost_report.cost_category_labour", False)
