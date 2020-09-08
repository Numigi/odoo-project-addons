# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import babel.dates
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round
from typing import Callable, Mapping
from .util import (
    CostReportCategory,
    TimeCategory,
    adjust_analytic_line_amount_sign,
    get_purchase_line_waiting_qty,
    get_waiting_for_invoice_total,
    group_analytic_lines,
    is_outsourcing_line,
    is_product_line,
    is_timesheet_line,
    purchase_line_is_waiting_invoice,
)


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

    def get_rendering_variables(self, projects, report_context=None):
        """Get the variables used for rendering the qweb report.

        :param project: the project.project recordset
        :param report_context: the rendering context
        :rtype: dict
        """
        report_context = report_context or {}

        print_date = self._get_print_date()

        product_categories = self._get_product_categories(projects, report_context)
        product_total = self._get_product_total(projects)
        product_sale_price = self._get_total_section_sale_price(product_categories)
        time_categories = self._get_time_categories(projects, report_context)
        time_total = self._get_time_total(projects)
        time_total_hours = self._get_time_total_hours(projects)
        time_sale_price = self._get_total_section_sale_price(time_categories)
        outsourcing_categories = self._get_outsourcing_categories(
            projects, report_context
        )
        outsourcing_total = self._get_outsourcing_total(projects)
        outsourcing_sale_price = self._get_total_section_sale_price(
            outsourcing_categories
        )

        total_cost = product_total + time_total + outsourcing_total
        total_sale_price = product_sale_price + time_sale_price + outsourcing_sale_price
        total_profit = total_sale_price - total_cost
        total_margin = (
            (total_profit / total_sale_price) * 100 if total_sale_price else 0
        )

        waiting_purchase_orders = self._get_waiting_purchase_orders(projects)
        waiting_purchase_orders_total = sum(
            get_waiting_for_invoice_total(o, projects) for o in waiting_purchase_orders
        )

        project = projects[:1]

        return {
            "adjust_analytic_line_amount_sign": adjust_analytic_line_amount_sign,
            "currency": project.company_id.currency_id,
            "is_outsourcing_line": is_outsourcing_line,
            "is_product_line": is_product_line,
            "is_timesheet_line": is_timesheet_line,
            "outsourcing_categories": outsourcing_categories,
            "outsourcing_total": outsourcing_total,
            "print_date": print_date,
            "product_categories": product_categories,
            "product_total": product_total,
            "project": project,
            "show_summary": report_context.get("show_summary", True),
            "time_categories": time_categories,
            "time_total": time_total,
            "time_total_hours": time_total_hours,
            "total_cost": float_round(total_cost, 2),
            "total_profit": float_round(total_profit, 2),
            "total_target_margin": float_round(total_margin, 2),
            "total_target_sale_price": float_round(total_sale_price, 2),
            "waiting_purchase_orders": waiting_purchase_orders,
            "waiting_purchase_order_total": float_round(
                waiting_purchase_orders_total, 2
            ),
            "get_waiting_for_invoice_total": get_waiting_for_invoice_total,
        }

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

    def _get_print_date(self):
        lang = self._context.get("lang") or "en_US"
        now = fields.Datetime.context_timestamp(self, datetime.now())
        return babel.dates.format_date(now, "long", locale=lang)

    def _get_product_categories(self, projects, report_context):
        """Get the stockable/consumable product categories."""
        lines = self._get_product_analytic_lines(projects)
        default_cost_category = self.env.ref(
            "project_cost_report.cost_category_product"
        )
        grouped_lines = group_analytic_lines(
            lines,
            lambda l: l.product_id.categ_id.project_cost_category_id
            or default_cost_category,
        )
        sorted_categories = sorted(grouped_lines.keys(), key=lambda c: c.name)
        unfolded_categories = report_context.get("unfolded_categories") or {}
        unfolded_product_categories = unfolded_categories.get("product") or []
        return [
            CostReportCategory(
                c,
                lines=grouped_lines.get(c),
                folded=c.id not in unfolded_product_categories,
            )
            for c in sorted_categories
        ]

    def _get_product_total(self, projects):
        lines = self._get_product_analytic_lines(projects)
        total_amount = sum(l.amount for l in lines)
        return float_round(-total_amount, 2)

    def _get_product_analytic_lines(self, projects):
        return projects.mapped("analytic_account_id.line_ids").filtered(
            lambda l: is_product_line(l)
        )

    def _get_time_categories(self, projects, report_context):
        """Get the task types for the TIME section."""
        lines = self._get_timesheet_analytic_lines(projects)
        default_cost_category = self.env.ref("project_cost_report.cost_category_labour")
        grouped_lines = group_analytic_lines(
            lines,
            lambda l: l.task_id.task_type_id.project_cost_category_id
            or default_cost_category,
        )
        sorted_categories = sorted(grouped_lines.keys(), key=lambda c: c.name or "")
        unfolded_categories = report_context.get("unfolded_categories") or {}
        unfolded_time_categories = unfolded_categories.get("time") or []
        return [
            TimeCategory(
                c,
                lines=grouped_lines.get(c),
                folded=c.id not in unfolded_time_categories,
            )
            for c in sorted_categories
        ]

    def _get_time_total(self, projects):
        lines = self._get_timesheet_analytic_lines(projects)
        total_amount = sum(l.amount for l in lines)
        return float_round(-total_amount, 2)

    def _get_time_total_hours(self, projects):
        lines = self._get_timesheet_analytic_lines(projects)
        total_hours = sum((l.unit_amount or 0) for l in lines)
        return float_round(total_hours, 2)

    def _get_timesheet_analytic_lines(self, projects):
        return projects.mapped("analytic_account_id.line_ids").filtered(
            lambda l: is_timesheet_line(l)
        )

    def _get_outsourcing_categories(self, projects, report_context):
        """Get the OUTSOURCING sections.

        Outsourcing has only one category (False).
        """
        unfolded_categories = report_context.get("unfolded_categories") or {}
        unfolded_outsourcing_categories = unfolded_categories.get("outsourcing") or []
        result = []
        lines = self._get_outsourcing_analytic_lines(projects)
        outsourcing_category = self.env.ref(
            "project_cost_report.cost_category_outsourcing"
        )

        if lines:
            empty_category = CostReportCategory(
                outsourcing_category,
                lines=lines,
                folded=outsourcing_category.id not in unfolded_outsourcing_categories,
            )
            result.append(empty_category)
        return result

    def _get_outsourcing_total(self, projects):
        lines = self._get_outsourcing_analytic_lines(projects)
        total_amount = sum(l.amount for l in lines)
        return float_round(-total_amount, 2)

    def _get_outsourcing_analytic_lines(self, projects):
        return projects.mapped("analytic_account_id.line_ids").filtered(
            lambda l: is_outsourcing_line(l)
        )

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

    def _get_total_section_sale_price(self, categories):
        return sum(c.target_sale_price for c in categories)
