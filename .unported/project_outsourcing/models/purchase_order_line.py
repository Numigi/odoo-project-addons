# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    is_outsourcing = fields.Boolean(related="order_id.is_outsourcing")

    @api.constrains("is_outsourcing", "product_id")
    def _check_if_is_outsourcing__product_is_service(self):
        outsourcing_lines = self.filtered(lambda l: l.is_outsourcing)
        for line in outsourcing_lines:
            if line.product_id.type == "product":
                raise ValidationError(
                    _(
                        "The product {product} can not be added to the outsourcing order "
                        "{order} because it is a stockable product. "
                        "Stockable products can not be used "
                        "on an outsourcing PO."
                    ).format(
                        product=line.product_id.display_name,
                        order=line.order_id.display_name,
                    )
                )

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if line.is_outsourcing:
            line.order_id._propagate_project_to_order_lines()
        return line
