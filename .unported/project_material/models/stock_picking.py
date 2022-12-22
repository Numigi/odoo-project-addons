# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockPicking(models.Model):

    _name = 'stock.picking'
    _inherit = ['stock.picking', 'project.select.mixin']

    task_id = fields.Many2one(
        'project.task',
        index=True,
        ondelete='restrict',
    )
    project_id = fields.Many2one(
        related='task_id.project_id', store=True,
        readonly=True,
    )

    task_readonly = fields.Boolean(compute='_compute_task_modifiers')
    task_invisible = fields.Boolean(compute='_compute_task_modifiers')
    task_required = fields.Boolean(compute='_compute_task_modifiers')

    def _compute_task_modifiers(self):
        for picking in self:
            picking_has_a_task = bool(picking.task_id)
            picking.task_readonly = True
            picking.task_invisible = False if picking_has_a_task else True
            picking.task_required = False
