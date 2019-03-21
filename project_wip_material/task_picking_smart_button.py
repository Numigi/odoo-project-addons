# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Task(models.Model):
    """Add the smart button to view the stock pickings."""

    _inherit = 'project.task'

    picking_count = fields.Integer(compute='_compute_consumption_pickings')
    picking_ids = fields.One2many(
        'stock.picking', string='Pickings',
        compute='_compute_consumption_pickings')

    def _compute_consumption_pickings(self):
        tasks_with_procurement_group = self.filtered(lambda t: t.procurement_group_id)
        for task in tasks_with_procurement_group:
            pickings = self.env['stock.picking'].search([
                ('group_id', '=', task.procurement_group_id.id),
            ])
            task.picking_ids = pickings
            task.picking_count = len(pickings)

    def open_picking_view_from_task(self):
        """Open the view of stock pickings related to the task.

        If there are multiple pickings, open the list view.
        Otherwise, open the form view.

        This method is inspired by the method action_view_delivery
        of sale.order. This method can be found at

        odoo/addons/sale_stock/models/sale_order.py
        """
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        if self.picking_count > 1:
            action['domain'] = [('id', 'in', self.picking_ids.ids)]

        else:
            picking_form_view = self.env.ref('stock.view_picking_form')
            action['views'] = [(picking_form_view.id, 'form')]
            action['res_id'] = self.picking_ids.id

        return action
