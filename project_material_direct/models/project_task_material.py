# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class TaskMaterialLine(models.Model):

    _inherit = "project.task.material"

    is_direct_consumption = fields.Boolean(readonly=True)
    origin_stock_move_id = fields.Many2one(
        "stock.move",
        "Stock Move",
    )
    origin_stock_picking_id = fields.Many2one(
        "stock.picking",
        "Stock Picking",
        related="origin_stock_move_id.picking_id",
    )
    direct_consumption_subtotal = fields.Float(
        "Direct Consumption Subtotal",
        compute="_compute_direct_consumption_subtotal",
    )

    @api.depends("consumed_qty", "unit_cost")
    def _compute_direct_consumption_subtotal(self):
        """Compute the direct consumption subtotal."""
        for line in self:
            line.direct_consumption_subtotal = line.consumed_qty * line.unit_cost

    def _should_generate_procurement(self):
        if self.is_direct_consumption:
            return False
        return super()._should_generate_procurement()

    @api.multi
    def write(self, vals):
        for line in self:
            if line.is_direct_consumption and not self.env.user._is_superuser():
                raise AccessError(
                    _(
                        "The material line {} was created from a direct consumption. "
                        "It can not be manually edited."
                    ).format(line.display_name)
                )
        return super().write(vals)

    @api.multi
    def unlink(self):
        for line in self:
            if line.is_direct_consumption:
                raise AccessError(
                    _(
                        "The material line {} was created from a direct consumption. "
                        "It can not be deleted."
                    ).format(line.display_name)
                )
        super().unlink()
