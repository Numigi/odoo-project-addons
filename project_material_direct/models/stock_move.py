# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    is_direct_consumption = fields.Boolean(
        related='picking_id.is_direct_consumption',
    )

    def _action_done(self):
        self._bind_direct_consumption_moves_to_picking_task()
        done_moves = super()._action_done()
        done_moves.sudo()._generate_direct_task_material_if_required()
        return done_moves

    def _bind_direct_consumption_moves_to_picking_task(self):
        direct_consumption_moves = self.filtered(lambda m: m.is_direct_consumption)
        for move in direct_consumption_moves:
            task = move.picking_id.task_id
            move.task_id = move.picking_id.task_id
            move.group_id = task._get_procurement_group()

    def _generate_direct_task_material_if_required(self):
        direct_consumption_moves = self.filtered(lambda m: m.is_direct_consumption)
        for move in direct_consumption_moves:
            move._generate_direct_task_material_line()

    def _generate_direct_task_material_line(self):
        vals = self._get_direct_material_line_vals()
        self.task_id.write({'direct_material_line_ids': [(0, 0, vals)]})

    def _get_direct_material_line_vals(self):
        return {
            'product_id': self.product_id.id,
            'initial_qty': 0,
            'move_ids': [(4, self.id)],
            'origin_stock_move_id': self.id,
            'is_direct_consumption': True,
        }
