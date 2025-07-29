# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TaskMaterialLine(models.Model):
    _inherit = "project.task.material"

    purchase_line_id = fields.Many2one(
        "purchase.order.line",
        "Purchase Order Line",
        ondelete="set null",
        index=True,
        copy=False,
    )
    purchase_id = fields.Many2one(
        "purchase.order",
        related="purchase_line_id.order_id",
        string="Related Document",
        store=True,
        readonly=True
    )
