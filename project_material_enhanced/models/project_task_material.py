# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTaskMaterial(models.Model):
    _inherit = "project.task.material"

    manufacturer = fields.Many2one(
        'res.partner',
        string='Manufacturer',
        related='product_id.manufacturer',
        store=True,
    )

    manufacturer_pref = fields.Char(
        string='Manuf. Product Code',
        related='product_id.manufacturer_pref',
        store=True,
    )

    available_qty = fields.Float(
        string='Available Quantity',
        compute='_compute_available_qty',
    )

    @api.depends('product_id')
    def _compute_available_qty(self):
        for record in self:
            quant = self.env['stock.quant'].search(
                [
                    ('product_id', '=', self.product_id.id),
                    ('location_id.usage', '=', 'internal'),
                    ('company_id', '=', self.company_id.id),
                ]
            )
            record.available_qty = sum(quant.mapped('available_quantity'))
