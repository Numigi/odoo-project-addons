# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.osv.expression import AND


class StockRule(models.Model):
    """Prevent stockable products from being added to a PO by stock rules."""

    _inherit = "stock.rule"

    def _make_po_get_domain(self, values, partner):
        domain = super()._make_po_get_domain(values, partner)
        return (*domain, ("is_outsourcing", "=", False))
