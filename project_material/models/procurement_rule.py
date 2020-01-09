# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class ProcurementRule(models.Model):

    _inherit = 'procurement.rule'

    def _get_stock_move_values(
        self, product_id, product_qty, product_uom,
        location_id, name, origin, values, group_id
    ):
        """Propagate material_line_id from procurement rule to stock move."""
        result = super()._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name,
            origin, values, group_id,
        )
        result['material_line_id'] = values.get('material_line_id')
        return result
