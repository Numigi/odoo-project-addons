# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPickingType(models.Model):

    _inherit = 'stock.picking.type'

    is_direct_consumption = fields.Boolean('Direct Consumption')

    @api.constrains('code', 'is_direct_consumption')
    def _check_is_direct_consumption(self):
        for picking_type in self:
            is_consumption = picking_type.code in ('consumption', 'consumption_return')
            if not is_consumption and picking_type.is_direct_consumption:
                raise ValidationError(_(
                    'Only operations of type Consumption or Consumption Return '
                    'can be defined as Direct Consumption.'
                ))
