# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AnalyticLine(models.Model):
    """Add extra computed fields to display in the report."""

    _inherit = "account.analytic.line"

    unit_cost = fields.Monetary(
        compute="_compute_unit_cost", currency_field="company_currency_id"
    )

    @api.depends("amount", "unit_amount")
    def _compute_unit_cost(self):
        for line in self:
            line.unit_cost = -(
                line.amount / line.unit_amount if line.unit_amount else 0
            )
