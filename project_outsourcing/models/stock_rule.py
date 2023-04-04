# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class StockRule(models.Model):
    """Prevent stockable products from being added to a PO by stock rules."""

    _inherit = "stock.rule"

    def _make_po_get_domain(self, company_id, values, partner):
        domain = super(StockRule, self)._make_po_get_domain(company_id, values,
                                                            partner)
        domain += (
            ('is_outsourcing', '=', False),
        )
        return domain
