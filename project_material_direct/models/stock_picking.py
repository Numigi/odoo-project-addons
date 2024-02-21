# © 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    is_direct_consumption = fields.Boolean(
        related='picking_type_id.is_direct_consumption',
    )

    def _compute_task_modifiers(self):
        super()._compute_task_modifiers()
        for picking in self:
            if picking.is_direct_consumption:
                picking.task_required = picking.state != 'done'
                picking.task_readonly = picking.state == 'done'
                picking.task_invisible = False

    @api.onchange('picking_type_id')
    def _onchange_picking_type_recompute_task_modifiers(self):
        self._compute_task_modifiers()
