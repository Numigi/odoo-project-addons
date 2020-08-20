# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    project_id = fields.Many2one(
        related='move_id.project_id', store=True,
        readonly=True
    )


