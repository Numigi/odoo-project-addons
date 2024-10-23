# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
        string='Available Quantity',
        related='product_id.free_qty',
        store=True,
    )
