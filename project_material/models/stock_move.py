# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    task_id = fields.Many2one(
        'project.task',
        index=True,
        ondelete='restrict',
        readonly=True,
    )
    project_id = fields.Many2one(related='task_id.project_id', store=True)
    material_line_id = fields.Many2one(
        'project.task.material',
        'Material Line',
        index=True,
        ondelete='restrict',
    )

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()
        vals['task_id'] = self.task_id.id
        return vals
