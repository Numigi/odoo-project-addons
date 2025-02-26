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
        store=True,
    )

    @api.depends('product_id', 'product_id.free_qty')
    def _compute_available_qty(self):
        for rec in self:
            warehouse_id = self.env['stock.warehouse'].search([
                ('company_id', '=', rec.company_id.id)], limit=1)
            rec.available_qty = rec.product_id.with_context(
                warehouse=warehouse_id.id).free_qty
