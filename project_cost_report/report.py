# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import babel.dates
from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round, float_compare
from odoo.exceptions import ValidationError
from typing import Callable, Mapping
from .tools import adjust_analytic_line_amount_sign


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

    _name = 'project.cost.report'
    _description = 'Project Cost Report'

    def _get_rendering_variables(self, project, report_context):
        """Get the variables used for rendering the qweb report.

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        lang = self._context.get('lang') or 'en_US'
        now = fields.Datetime.context_timestamp(self, datetime.now())
        return {
            'project': project,
            'currency': project.company_id.currency_id,
            'print_date': babel.dates.format_date(now, 'long', locale=lang),
            'adjust_analytic_line_amount_sign': adjust_analytic_line_amount_sign,
        }

    def get_project_from_report_context(self, report_context):
        """Get the project record from the given report context.

        :param report_context: the rendering context
        :return: a project.project singleton
        """
        project_id = report_context.get('active_id')

        if not project_id:
            raise ValidationError(_(
                'The cost report was triggered without a project ID in context.'
            ))

        return self.env['project.project'].browse(project_id)

    @api.model
    def get_html(self, report_context):
        """Get the report html given the report context.

        :param dict report_context: the report context.
        :rtype: bytes
        """
        project = self.get_project_from_report_context(report_context)
        rendering_variables = self._get_rendering_variables(project, report_context)
        return self.env.ref('project_cost_report.cost_report_html').render(rendering_variables)

    @api.model
    def get_pdf(self, report_context):
        """Get the report html given the report context.

        :param dict report_context: the report context.
        :rtype: bytes
        """
        project = self.get_project_from_report_context(report_context)
        rendering_variables = self._get_rendering_variables(project, report_context)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        rendering_variables.update({
            'mode': 'print',
            'base_url': base_url,
        })
        body = self.env['ir.ui.view'].render_template(
            "project_cost_report.cost_report_pdf",
            values=rendering_variables,
        )
        header = self.env['ir.actions.report'].render_template(
            "web.minimal_layout", values=rendering_variables
        )
        return self.env['ir.actions.report']._run_wkhtmltopdf(
            [body],
            header=header,
            landscape=True,
            specific_paperformat_args={
                'data-report-margin-top': 10,
                'data-report-header-spacing': 10
            }
        )

    @api.model
    def get_foldable_categories(self, project_id):
        """Get a dictionary containing all the foldable categories for the report.

        Here is an example of expected result:

        {
            'product': [1, 13, 53, 27],
            'time': [1, 4, 5],
            'outsourcing': [954, 1058],
        }

        The IDS contained in each category depends on the model used to group
        analytic lines in each category.

        :param int project_id: the ID of the project
        :rtype: Mapping[str, List[int]]
        """
        return {}


def _group_analytic_lines(lines: models.Model, key: Callable) -> Mapping[object, models.Model]:
    grouped_lines = {}
    for line in lines:
        key_ = key(line)
        if key_ not in grouped_lines:
            grouped_lines[key_] = lines.env['account.analytic.line']
        grouped_lines[key_] |= line
    return grouped_lines


class CostReportCategory:
    """Cost report category.

    This class is used to simplify the qWeb templates.
    It contains the data related to a category of the report.
    """

    def __init__(self, id_: int, name: str, lines: models.Model, folded: bool):
        """Initialize the report category.

        :param id: the ID of the related product.category record
        :param name: the name of the category
        :param lines: a recordset of Odoo account.analytic.line
        :param folded: whether the category is folded or not
        """
        self.id = id_
        self.name = name
        self.lines = lines
        self.folded = folded
        self.total = float_round(sum(-l.amount for l in lines), 2)


class ProjectCostReportWithProducts(models.TransientModel):

    _inherit = 'project.cost.report'

    def _get_product_analytic_line_domain(self, project):
        """Get the search domain to query time stockable/consumable product lines.

        :param project: the project.project record
        :rtype: list
        """
        return [
            ('account_id', '=', project.analytic_account_id.id),
            ('product_id.type', 'in', ('product', 'consu')),
            ('revenue', '=', False),
        ]

    def _get_product_categories(self, project, report_context):
        """Get the stockable/consumable product categories.

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        domain = self._get_product_analytic_line_domain(project)
        lines = self.env['account.analytic.line'].search(domain)
        grouped_lines = _group_analytic_lines(lines, lambda l: l.product_id.categ_id)
        sorted_categories = sorted(grouped_lines.keys(), key=lambda c: c.name)
        unfolded_categories = report_context.get('unfolded_categories') or {}
        unfolded_product_categories = unfolded_categories.get('product') or []
        return [
            CostReportCategory(
                id_=c.id,
                name=c.name,
                lines=grouped_lines.get(c),
                folded=c.id not in unfolded_product_categories
            ) for c in sorted_categories
        ]

    def _get_product_total(self, project):
        """Get the total amount for the PRODUCTS section.

        :param project: the project.project record
        :rtype: float
        """
        domain = self._get_product_analytic_line_domain(project)
        result = self.env['account.analytic.line'].read_group(
            domain=domain, fields=['account_id', 'amount'], groupby='account_id')
        amount = result[0]['amount'] if result else 0
        return float_round(-amount, 2)

    def _get_rendering_variables(self, project, report_context):
        """Add the variables related to the PRODUCTS section."""
        res = super()._get_rendering_variables(project, report_context)
        res.update({
            'product_categories': self._get_product_categories(project, report_context),
            'product_total': self._get_product_total(project),
        })
        return res

    @api.model
    def get_foldable_categories(self, project_id):
        """Add product categories to foldable categories."""
        res = super().get_foldable_categories(project_id)
        project = self.env['project.project'].browse(project_id)
        domain = self._get_product_analytic_line_domain(project)
        analytic_lines = self.env['account.analytic.line'].search(domain)
        res['product'] = analytic_lines.mapped('product_id.categ_id.id')
        return res


class TimeCategory(CostReportCategory):
    """Categories used for the TIME section.

    These categories have one more field to display: the total hours.

    The total of units can not be used on other sections because
    other sections mix different units of measure.
    """

    def __init__(self, id_: int, name: str, lines: models.Model, folded: bool):
        super().__init__(id_, name, lines, folded)
        self.total_hours = float_round(sum(l.unit_amount for l in lines), 2)


class ProjectCostReportWithTime(models.TransientModel):

    _inherit = 'project.cost.report'

    def _get_empty_task_type_label(self):
        """Get the label to display on the empty time category.

        The empty category is the category that groups
        timesheet lines that are not bound to a task type.

        :rtype: str
        """
        return _('Labour')

    def _get_time_analytic_line_domain(self, project):
        """Get the search domain to query time analytic lines.

        :param project: the project.project record
        :rtype: list
        """
        return [
            ('account_id', '=', project.analytic_account_id.id),
            ('task_id', '!=', False),
            ('revenue', '=', False),
        ]

    def _get_time_categories(self, project, report_context):
        """Get the task types for the TIME section.

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        domain = self._get_time_analytic_line_domain(project)
        lines = self.env['account.analytic.line'].search(domain)
        grouped_lines = _group_analytic_lines(lines, lambda l: l.task_id.task_type_id)
        sorted_categories = sorted(grouped_lines.keys(), key=lambda c: c.name or "")
        unfolded_categories = report_context.get('unfolded_categories') or {}
        unfolded_time_categories = unfolded_categories.get('time') or []
        return [
            TimeCategory(
                id_=c.id,
                name=c.name or self._get_empty_task_type_label(),
                lines=grouped_lines.get(c),
                folded=c.id not in unfolded_time_categories
            ) for c in sorted_categories
        ]

    def _get_time_total(self, project):
        """Get the total amount for the TIME section.

        :param project: the project.project record
        :rtype: float
        """
        domain = self._get_time_analytic_line_domain(project)
        result = self.env['account.analytic.line'].read_group(
            domain=domain, fields=['account_id', 'amount'], groupby='account_id')
        amount = result[0]['amount'] if result else 0
        return float_round(-amount, 2)

    def _get_time_total_hours(self, project):
        """Get the total hours (units) for the TIME section.

        :param project: the project.project record
        :rtype: float
        """
        domain = self._get_time_analytic_line_domain(project)
        result = self.env['account.analytic.line'].read_group(
            domain=domain, fields=['account_id', 'unit_amount'], groupby='account_id')
        amount = result[0]['unit_amount'] if result else 0
        return float_round(amount, 2)

    def _get_rendering_variables(self, project, report_context):
        """Add the variables related to the TIME section."""
        res = super()._get_rendering_variables(project, report_context)
        res.update({
            'time_categories': self._get_time_categories(project, report_context),
            'time_total': self._get_time_total(project),
            'time_total_hours': self._get_time_total_hours(project),
        })
        return res

    @api.model
    def get_foldable_categories(self, project_id):
        """Add time categories to foldable categories."""
        res = super().get_foldable_categories(project_id)
        project = self.env['project.project'].browse(project_id)
        domain = self._get_time_analytic_line_domain(project)
        analytic_lines = self.env['account.analytic.line'].search(domain)
        res['time'] = analytic_lines.mapped('task_id.task_type_id.id')
        res['time'].append(False)  # Empty task type category (Labour)
        return res


class ProjectCostReportWithOutsourcing(models.TransientModel):

    _inherit = 'project.cost.report'

    def _get_empty_outsourcing_category_label(self):
        """Get the label to display on the unique outsourcing category.

        :rtype: str
        """
        return _('Outsourcing')

    def _get_outsourcing_analytic_line_domain(self, project):
        """Get the search domain to query outsourcing analytic lines.

        :param project: the project.project record
        :rtype: list
        """
        return [
            ('account_id', '=', project.analytic_account_id.id),
            ('task_id', '=', False),
            ('product_id.type', '=', 'service'),
            ('revenue', '=', False),
        ]

    def _get_outsourcing_categories(self, project, report_context):
        """Get the OUTSOURCING sections.

        Outsourcing has only one category (False).

        :param project: the project.project record
        :param report_context: the rendering context
        :rtype: dict
        """
        domain = self._get_outsourcing_analytic_line_domain(project)
        unfolded_categories = report_context.get('unfolded_categories') or {}
        unfolded_outsourcing_categories = unfolded_categories.get('outsourcing') or []
        result = []
        lines = self.env['account.analytic.line'].search(domain)
        if lines:
            empty_category = CostReportCategory(
                id_=False,
                name=self._get_empty_outsourcing_category_label(),
                lines=lines,
                folded=False not in unfolded_outsourcing_categories
            )
            result.append(empty_category)
        return result

    def _get_outsourcing_total(self, project):
        """Get the total amount for the OUTSOURCING section.

        :param project: the project.project record
        :rtype: float
        """
        domain = self._get_outsourcing_analytic_line_domain(project)
        result = self.env['account.analytic.line'].read_group(
            domain=domain, fields=['account_id', 'amount'], groupby='account_id')
        amount = result[0]['amount'] if result else 0
        return float_round(-amount, 2)

    def _get_rendering_variables(self, project, report_context):
        """Add the variables related to the OUTSOURCING section."""
        res = super()._get_rendering_variables(project, report_context)
        res.update({
            'outsourcing_categories': self._get_outsourcing_categories(project, report_context),
            'outsourcing_total': self._get_outsourcing_total(project),
        })
        return res

    @api.model
    def get_foldable_categories(self, project_id):
        """Add outsourcing categories to foldable categories.

        The OUTSOURCING section has only one category (the empty category).
        """
        res = super().get_foldable_categories(project_id)
        res['outsourcing'] = [False]
        return res


class ProjectCostReportWithTotalCost(models.TransientModel):

    _inherit = 'project.cost.report'

    def _get_rendering_variables(self, project, report_context):
        """Add the total of costs to the rendering variables."""
        res = super()._get_rendering_variables(project, report_context)
        res.update({
            'total_cost': float_round(
                res['product_total'] + res['time_total'] + res['outsourcing_total'], 2
            )
        })
        return res


def purchase_line_is_waiting_invoice(line: models.Model) -> bool:
    """Determine whether a purchase line is waiting an invoice.

    :param line: a purchase.order.line singleton
    """
    precision = line.env['decimal.precision'].precision_get('Product Unit of Measure')
    less_units_invoiced_than_purchased = (
        float_compare(line.qty_invoiced, line.product_qty, precision_digits=precision) == -1
    )
    return less_units_invoiced_than_purchased


def get_purchase_line_waiting_qty(line: models.Model) -> float:
    """Get the quantity of units waiting invoices from a purchase line.

    :param line: a purchase.order.line singleton
    """
    precision = line.env['decimal.precision'].precision_get('Product Unit of Measure')
    return float_round(line.product_qty - line.qty_invoiced, precision_digits=precision)


def get_waiting_for_invoice_total(order: models.Model, project: models.Model):
    """Get the total amount waiting for invoices for a purchase order.

    :param order: the purchase order record.
    :param project: the project for which to render the report.
    :return: the amount waiting for invoices
    """
    lines_waiting_invoices = order.order_line.filtered(
        lambda l: purchase_line_is_waiting_invoice(l) and
        l.account_analytic_id == project.analytic_account_id
    )

    return float_round(
        sum(l.price_unit * get_purchase_line_waiting_qty(l)
            for l in lines_waiting_invoices),
        2
    )


class ProjectCostReportWithWaitingInvoices(models.TransientModel):

    _inherit = 'project.cost.report'

    def _get_waiting_purchase_order_lines(self, project):
        """Get the purchase order lines with unreceived invoices.

        :param project: the project.project record
        :rtype: purchase.order.line
        """
        domain = [
            ('account_analytic_id', '=', project.analytic_account_id.id),
            ('order_id.state', 'in', ('purchase', 'done')),
        ]
        lines = self.env['purchase.order.line'].search(domain)
        return lines.filtered(lambda l: purchase_line_is_waiting_invoice(l))

    def _get_waiting_purchase_orders(self, project):
        """Get the purchase orders with unreceived invoices.

        :param project: the project.project record
        :rtype: List[waitingPurchaseOrder]
        """
        lines = self._get_waiting_purchase_order_lines(project)
        return lines.mapped('order_id').sorted(key=lambda o: o.name)

    def _get_rendering_variables(self, project, report_context):
        """Add waiting purchase orders to the rendering context."""
        result = super()._get_rendering_variables(project, report_context)
        orders = self._get_waiting_purchase_orders(project)
        result['waiting_purchase_orders'] = orders
        result['waiting_purchase_order_total'] = float_round(
            sum(get_waiting_for_invoice_total(o, project) for o in orders), 2
        )
        result['get_waiting_for_invoice_total'] = get_waiting_for_invoice_total
        return result
