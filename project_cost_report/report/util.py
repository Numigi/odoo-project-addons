from odoo.tools.float_utils import float_round, float_compare


class CostReportCategory:
    """Cost report category.

    This class is used to simplify the qWeb templates.
    It contains the data related to a category of the report.
    """

    def __init__(self, category, lines, folded):
        self.category = category
        self.id = category.id
        self.name = category.name
        self.lines = lines
        self.folded = folded
        self.total = float_round(sum(-l.amount for l in lines), 2)
        self.target_margin = category.target_margin

    @property
    def target_sale_price(self):
        sale_price_ratio = 1 - self.target_margin / 100
        return float_round(self.total / sale_price_ratio if sale_price_ratio else 0, 2)

    @property
    def target_profit(self):
        return float_round(self.target_sale_price - self.total, 2)


class TimeCategory(CostReportCategory):
    """Categories used for the TIME section.

    These categories have one more field to display: the total hours.

    The total of units can not be used on other sections because
    other sections mix different units of measure.
    """

    def __init__(self, category, lines, folded):
        super().__init__(category, lines, folded)
        self.total_hours = float_round(sum(l.unit_amount for l in lines), 2)
        self.target_hourly_rate = category.target_hourly_rate

    @property
    def target_sale_price(self):
        return float_round(self.total_hours * self.target_hourly_rate, 2)


def is_timesheet_line(analytic_line):
    return not analytic_line.revenue and analytic_line.project_id


def is_product_line(analytic_line):
    return (
        not analytic_line.project_id
        and not analytic_line.revenue
        and analytic_line.product_id.type in ("consu", "product")
    )


def is_outsourcing_line(analytic_line):
    return (
        not analytic_line.revenue
        and not analytic_line.project_id
        and analytic_line.product_id.type == "service"
    )


def adjust_analytic_line_amount_sign(line, amount):
    """Adjust the amount sign of an analytic line for the cost report.

    Analytic lines generated from outgoing stock moves have a negative
    quantites. Lines from incoming moves have positive quantities.

    In other context, this behavior could be accurate.

    In the cost report, we wish to display the contrary.

    This function adjusts the sign of the given amount from an analytic line.
    If the analytic line is bound to a stock move, the amount sign
    will be reversed. Otherwise, the amount is unchanged.

    :param line: the analytic line
    :param amount: the amount to display in the report
    :return: the adjusted amount.
    """
    is_bound_to_stock_move = bool(line.move_id.move_id.stock_move_id)
    return -(amount or 0) if is_bound_to_stock_move else amount


def group_analytic_lines(lines, key):
    grouped_lines = {}
    for line in lines:
        key_ = key(line)
        if key_ not in grouped_lines:
            grouped_lines[key_] = lines.env["account.analytic.line"]
        grouped_lines[key_] |= line
    return grouped_lines


def purchase_line_is_waiting_invoice(line):
    """Determine whether a purchase line is waiting an invoice.

    :param line: a purchase.order.line singleton
    """
    precision = line.env["decimal.precision"].precision_get("Product Unit of Measure")
    less_units_invoiced_than_purchased = (
        float_compare(line.qty_invoiced, line.product_qty, precision_digits=precision)
        == -1
    )
    return less_units_invoiced_than_purchased


def get_purchase_line_waiting_qty(line):
    """Get the quantity of units waiting invoices from a purchase line.

    :param line: a purchase.order.line singleton
    """
    precision = line.env["decimal.precision"].precision_get("Product Unit of Measure")
    return float_round(line.product_qty - line.qty_invoiced, precision_digits=precision)


def get_waiting_for_invoice_total(order, projects):
    """Get the total amount waiting for invoices for a purchase order.

    :param order: the purchase order record.
    :param project: the project for which to render the report.
    :return: the amount waiting for invoices
    """
    analytic_accounts = projects.mapped("analytic_account_id")
    lines_waiting_invoices = order.order_line.filtered(
        lambda l: purchase_line_is_waiting_invoice(l)
        and l.account_analytic_id in analytic_accounts
    )
    return float_round(
        sum(
            l.price_unit * get_purchase_line_waiting_qty(l)
            for l in lines_waiting_invoices
        ),
        2,
    )
