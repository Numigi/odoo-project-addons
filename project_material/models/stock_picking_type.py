# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPickingType(models.Model):
    """Add consumption to picking type codes."""

    _inherit = "stock.picking.type"

    code = fields.Selection(
        selection_add=[
            ("consumption", "Consumption"),
            ("consumption_return", "Consumption Return"),
        ], ondelete={'consumption': 'cascade', 'consumption_return': 'cascade', }
    )
