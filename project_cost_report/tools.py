# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from typing import Optional


def adjust_analytic_line_amount_sign(
    line: models.Model, amount: Optional[float]
) -> float:
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
