# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    task_id = fields.Many2one(
        "project.task",
        index=True,
        ondelete="restrict",
        readonly=True,
    )

    project_id = fields.Many2one(
        related="task_id.project_id",
        store=True,
        readonly=True,
    )
    material_line_id = fields.Many2one(
        "project.task.material",
        "Material Line",
        index=True,
        ondelete="restrict",
    )

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        vals["task_id"] = self.task_id.id
        return vals

    def _prepare_procurement_values(self):
        vals = super()._prepare_procurement_values()
        vals["task_id"] = self.task_id.id
        return vals


class StockMoveWithNoAggregation(models.Model):
    """Prevent the aggregation of stock moves generated from a material line.

    If a task has 2 material lines with the same product, then each line must generate
    a separate chain of stock moves.
    """

    _inherit = "stock.move"

    destination_material_line_id = fields.Many2one(
        "project.task.material",
        "Destination Material Line",
        compute="_compute_destination_material_line_id",
        store=True,
    )

    @api.depends("material_line_id", "move_dest_ids")
    def _compute_destination_material_line_id(self):
        for move in self:
            move.destination_material_line_id = move._find_destination_material_line()

    def _find_destination_material_line(self):
        if self.material_line_id:
            return self.material_line_id

        if self.origin_returned_move_id:
            return self.origin_returned_move_id._find_destination_material_line()

        return self.mapped("move_dest_ids.material_line_id")[:1]

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        result = super()._prepare_merge_moves_distinct_fields()
        result.append("destination_material_line_id")
        return result

    @api.model
    def _prepare_merge_move_sort_method(self, move):
        result = super()._prepare_merge_move_sort_method(move)
        result.append(move.destination_material_line_id.id)
        return result
