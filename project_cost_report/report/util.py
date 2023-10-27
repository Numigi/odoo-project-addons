from odoo.tools.float_utils import float_round, float_compare


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
            l.price_unit * _get_purchase_line_waiting_qty(l)
            for l in lines_waiting_invoices
        ),
        2,
    )


def _get_purchase_line_waiting_qty(line):
    """Get the quantity of units waiting invoices from a purchase line.

    :param line: a purchase.order.line singleton
    """
    precision = line.env["decimal.precision"].precision_get("Product Unit of Measure")
    return float_round(line.product_qty - line.qty_invoiced, precision_digits=precision)
