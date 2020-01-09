# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    task_id = fields.Many2one(related='group_id.task_id', store=True)
    project_id = fields.Many2one(related='group_id.project_id', store=True)
