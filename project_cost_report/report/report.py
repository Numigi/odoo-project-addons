# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import babel.dates
from datetime import datetime
from itertools import chain
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round
from typing import Callable, Mapping
from .util import (
    adjust_analytic_line_amount_sign,
    get_waiting_for_invoice_total,
    group_analytic_lines,
    purchase_line_is_waiting_invoice,
)
from .report_category import CostReportCategory


SECTION_TITLES = {
    "supply": _("Shop Supply"),
    "products": _("Products"),
    "time": _("Time"),
    "outsourcing": _("Outsourcing"),
}


class ProjectCostReport(models.TransientModel):
    """Project Cost Report.

    This model is used to generate the cost report.

    The report is structured as follow:

    SECTION 1
    ---------

    Category 1.1
    ~~~~~~~~~~~~
    Analytic Line 1.1.1
    Analytic Line 1.1.2

    Category 1.2
    ~~~~~~~~~~~~
    Analytic Line 1.2.1

    SECTION 2
    ---------

    Category 2.1
    ~~~~~~~~~~~~
    Analytic Line 2.1.1
    ...

    The report sections are static (defined in the code):

    * PRODUCTS
    * TIME
    * OUTSOURCING
    * etc

    The categories are dynamic.
    The grouping key of each category is different:

    * Categories under PRODUCTS are product categories.
    * Categories under TIME are task types.
    * OUTSOURCING has only one category (Outsourcing).

    Each category contains a given recordset of analytic lines.

    If a report category has no analytic line, it is not shown.
    """

    _name = "project.cost.report"
    _description = "Project Cost Report"

    @api.model
    def get_html(self, report_context):
        """Get the report html given the report context.

        :param dict report_context: the report context.
        :rtype: bytes
        """
        project = self.get_project_from_report_context(report_context)
        rendering_variables = self.get_rendering_variables(project, report_context)
        return self.env.ref("project_cost_report.cost_report_html").render(
            rendering_variables
        )

    @api.model
    def get_pdf(self, report_context):
        """Get the report html given the report context.

        :param dict report_context: the report context.
        :rtype: bytes
        """
        project = self.get_project_from_report_context(report_context)
        rendering_variables = self.get_rendering_variables(project, report_context)
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        rendering_variables.update({"mode": "print", "base_url": base_url})
        body = self.env["ir.ui.view"].render_template(
            "project_cost_report.cost_report_pdf", values=rendering_variables
        )
        header = self.env["ir.actions.report"].render_template(
            "web.minimal_layout", values=rendering_variables
        )
        return self.env["ir.actions.report"]._run_wkhtmltopdf(
            [body],
            header=header,
            landscape=True,
            specific_paperformat_args={
                "data-report-margin-top": 10,
                "data-report-header-spacing": 10,
            },
        )

    def get_project_from_report_context(self, report_context):
        """Get the project record from the given report context.

        :param report_context: the rendering context
        :return: a project.project singleton
        """
        project_id = report_context.get("active_id")

        if not project_id:
            raise ValidationError(
                _("The cost report was triggered without a project ID in context.")
            )

        return self.env["project.project"].browse(project_id)

    def get_rendering_variables(self, projects, report_context=None):
        """Get the variables used for rendering the qweb report.

        :param project: the project.project recordset
        :param report_context: the rendering context
        :rtype: dict
        """
        report_context = report_context or {}

        print_date = self._get_print_date()

        waiting_purchase_orders = self._get_waiting_purchase_orders(projects)
        waiting_purchase_orders_total = sum(
            get_waiting_for_invoice_total(o, projects) for o in waiting_purchase_orders
        )

        project = projects[:1]

        sections = self._get_sections(projects, report_context)

        cost = sum(s["cost"] for s in sections)
        revenue = sum(s["revenue"] for s in sections)
        profit = sum(s["profit"] for s in sections)
        total_hours = sum(s["total_hours"] for s in sections)
        target_sale_price = sum(s["target_sale_price"] for s in sections)
        target_profit = sum(s["target_profit"] for s in sections)
        target_margin = (
            (target_profit / target_sale_price) * 100 if target_sale_price else 0
        )
        profit_percent = (profit / revenue) * 100 if revenue else 0

        return {
            "project": project,
            "print_date": print_date,
            "currency": project.currency_id,
            "show_summary": report_context.get("show_summary", False),
            # Sections
            "sections": sections,
            "cost": float_round(cost, 2),
            "revenue": float_round(revenue, 2),
            "profit": float_round(profit, 2),
            "profit_percent": float_round(profit_percent, 2),
            "target_sale_price": float_round(target_sale_price, 2),
            "target_profit": float_round(target_profit, 2),
            "target_margin": float_round(target_margin, 2),
            "total_hours": float_round(total_hours, 2),
            # Waiting For Purchase Order
            "waiting_purchase_orders": waiting_purchase_orders,
            "waiting_purchase_order_total": float_round(
                waiting_purchase_orders_total, 2
            ),
            # Utilities
            "adjust_analytic_line_amount_sign": adjust_analytic_line_amount_sign,
            "get_waiting_for_invoice_total": get_waiting_for_invoice_total,
        }

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

    def _get_section_categories(self, projects, report_context, section_name):
        all_lines = projects.mapped("analytic_account_id.line_ids")
        section_lines = all_lines.filtered(
            lambda l: l.project_cost_section == section_name
        )
        grouped_lines = group_analytic_lines(
            section_lines, lambda l: l.project_cost_category_id
        )

        sorted_categories = sorted(grouped_lines.keys(), key=lambda c: c.sequence or 0)

        unfolded_categories = report_context.get("unfolded_categories") or []

        return [
            CostReportCategory(
                section_name,
                category,
                lines=grouped_lines.get(category),
                folded=category.id not in unfolded_categories,
            )
            for category in sorted_categories
        ]

    def _get_print_date(self):
        lang = self._context.get("lang") or "en_US"
        now = fields.Datetime.context_timestamp(self, datetime.now())
        return babel.dates.format_date(now, "long", locale=lang)

    def _get_waiting_purchase_order_lines(self, projects):
        """Get the purchase order lines with unreceived invoices.

        :param project: the project.project record
        :rtype: purchase.order.line
        """
        domain = [
            ("account_analytic_id", "in", projects.mapped("analytic_account_id").ids),
            ("order_id.state", "in", ("purchase", "done")),
        ]
        lines = self.env["purchase.order.line"].search(domain)
        return lines.filtered(lambda l: purchase_line_is_waiting_invoice(l))

    def _get_waiting_purchase_orders(self, projects):
        """Get the purchase orders with unreceived invoices.

        :param project: the project.project record
        :rtype: List[waitingPurchaseOrder]
        """
        lines = self._get_waiting_purchase_order_lines(projects)
        return lines.mapped("order_id").sorted(key=lambda o: o.name)

    @api.model
    def category_cost_clicked(self, report_context, section, category_id):
        project = self.get_project_from_report_context(report_context)
        category = self._get_category(category_id)
        action = self._get_analytic_line_action()
        action["name"] = _("({category}) - Cost").format(category=category.display_name)
        action["domain"] = [
            ("account_id", "=", project.analytic_account_id.id),
            ("revenue", "=", False),
            ("project_cost_section", "=", section),
            ("project_cost_category_id", "=", category.id),
        ]
        return action

    @api.model
    def category_revenue_clicked(self, report_context, section, category_id):
        project = self.get_project_from_report_context(report_context)
        category = self._get_category(category_id)
        action = self._get_analytic_line_action()
        action["name"] = _("({category}) - Revenue").format(
            category=category.display_name
        )
        action["domain"] = [
            ("account_id", "=", project.analytic_account_id.id),
            ("revenue", "=", True),
            ("project_cost_section", "=", section),
            ("project_cost_category_id", "=", category.id),
        ]
        return action

    @api.model
    def category_profit_clicked(self, report_context, section, category_id):
        project = self.get_project_from_report_context(report_context)
        category = self._get_category(category_id)
        action = self._get_analytic_line_action()
        action["name"] = _("({category}) - Profit").format(
            category=category.display_name
        )
        action["domain"] = [
            ("account_id", "=", project.analytic_account_id.id),
            ("project_cost_section", "=", section),
            ("project_cost_category_id", "=", category.id),
        ]
        return action

    def _get_analytic_line_action(self):
        list_view_id = self.env.ref("analytic.view_account_analytic_line_tree").id
        return {
            "res_model": "account.analytic.line",
            "views": [[list_view_id, "list"], [False, "form"]],
            "type": "ir.actions.act_window",
            "target": "current",
        }

    @api.model
    def analytic_line_clicked(self, line_id):
        line = self.env["account.analytic.line"].browse(line_id)
        return {
            "res_model": "account.analytic.line",
            "views": [[False, "form"]],
            "type": "ir.actions.act_window",
            "target": "current",
            "view_type": "form",
            "res_id": line_id,
            "name": line.display_name,
        }

    def _get_category(self, category_id):
        return self.env["project.cost.category"].browse(category_id)
