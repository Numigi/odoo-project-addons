# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.tools import float_round


class ProjectTaskMaterial(models.Model):
    _inherit = "project.task.material"

    manufacturer = fields.Many2one(
        'res.partner',
        string='Manufacturer',
        related='product_id.manufacturer',
        store=True,
    )

    manufacturer_pname = fields.Char(
        string='Manuf. Product Name',
        related='product_id.manufacturer_pname',
        store=True,
    )

    available_qty = fields.Float(
        string='Available Quantity', compute='_compute_available_qty_not_res'
    )

    @api.depends("product_id")
    def _compute_available_qty_not_res(self):
        for material in self:
            res = material._compute_product_available_not_res_dict()
            qty = res[material.product_id.id]["qty_available_not_res"]
            material.available_qty = qty
        return res

    def _compute_product_available_not_res_dict(self):
        res = {}

        domain_quant = self._prepare_domain_available_not_reserved()
        quants = (
            self.env["stock.quant"]
            .with_context(lang=False)
            .read_group(
                domain_quant,
                ["product_id", "location_id", "quantity", "reserved_quantity"],
                ["product_id", "location_id"],
                lazy=False,
            )
        )
        self._set_stock_available_not_reserved_values(res, quants)
        return res

    def _prepare_domain_available_not_reserved(self):
        domain_quant = [("product_id", "in", self.mapped('product_id').ids)]
        domain_quant_locations = self.product_id._get_domain_locations()[0]
        domain_quant.extend(domain_quant_locations)
        return domain_quant

    def _set_stock_available_not_reserved_values(self, result, quants):
        product_sums = {}
        rounding = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure'
        )
        for quant in quants:
            product_sums.setdefault(quant["product_id"][0], 0.0)
            product_sums[quant["product_id"][0]] += (
                quant["quantity"] - quant["reserved_quantity"]
            )
        for material in self.with_context(prefetch_fields=False, lang=""):
            available_not_res = float_round(
                product_sums.get(material.product_id.id, 0.0),
                precision_rounding=material.product_id.uom_id.rounding or rounding,
            )
            result[material.product_id.id] = {
                "qty_available_not_res": available_not_res
            }
