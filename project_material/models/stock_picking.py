# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class StockPicking(models.Model):

    _name = 'stock.picking'
    _inherit = ['stock.picking', 'project.select.mixin']

    task_id = fields.Many2one(
        'project.task',
        index=True,
        ondelete='restrict',
        readonly=True,
    )
    project_id = fields.Many2one(related='task_id.project_id', store=True)
