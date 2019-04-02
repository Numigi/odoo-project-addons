# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.addons.purchase.models.purchase import PurchaseOrder
from odoo.exceptions import ValidationError

READONLY_STATES = PurchaseOrder.READONLY_STATES


class PurchaseOrderWithOutSourcing(models.Model):

    _inherit = 'purchase.order'

    is_outsourcing = fields.Boolean(
        'Outsourcing',
        track_visibility='onchange',
        states=READONLY_STATES,
    )

    project_id = fields.Many2one(
        'project.project', 'Project', ondelete='restrict',
        track_visibility='onchange',
        states=READONLY_STATES,
    )

    task_id = fields.Many2one(
        'project.task', 'Task', ondelete='restrict',
        track_visibility='onchange',
        states=READONLY_STATES,
    )

    @api.onchange('is_outsourcing')
    def _on_empty_outsourcing__empty_project_and_task(self):
        if not self.is_outsourcing:
            self.project_id = False
            self.task_id = False

    @api.constrains('is_outsourcing', 'task_id')
    def _check_if_is_outsourcing__task_required(self):
        outsourcing_orders = self.filtered(lambda o: o.is_outsourcing)
        for order in outsourcing_orders:
            if not order.task_id:
                raise ValidationError(_(
                    "The purchase order {} must have a task because "
                    "it is an outsourcing PO."
                ).format(order.display_name))

    @api.constrains('is_outsourcing', 'project_id')
    def _check_if_is_outsourcing__project_required(self):
        outsourcing_orders = self.filtered(lambda o: o.is_outsourcing)
        for order in outsourcing_orders:
            if not order.project_id:
                raise ValidationError(_(
                    "The purchase order {} must have a project because "
                    "it is an outsourcing PO."
                ).format(order.display_name))

    def _propagate_project_to_order_lines(self):
        lines_with_different_project = self.order_line.filtered(
            lambda l: l.account_analytic_id != self.project_id.analytic_account_id
        )
        lines_with_different_project.write({
            'account_analytic_id': self.project_id.analytic_account_id.id,
        })

    @api.model
    def create(self, vals):
        order = super().create(vals)
        order._propagate_project_to_order_lines()
        return order

    @api.multi
    def write(self, vals):
        super().write(vals)
        outsourcing_orders = self.filtered(lambda o: o.is_outsourcing)
        for order in outsourcing_orders:
            order._propagate_project_to_order_lines()
        return True

    @api.onchange('project_id')
    def _onchange_project__propagate_analytic_account(self):
        if self.is_outsourcing:
            for line in self.order_line:
                line.account_analytic_id = self.project_id.analytic_account_id

    def _check_outsourcing_project_has_type(self):
        if not self.project_id.project_type_id:
            raise ValidationError(_(
                'The project {} has no type. '
                'The project type must be set before confirming the '
                'outsourcing purchase order.'
            ).format(self.project_id.display_name))

    def _check_outsourcing_project_type_has_wip_account(self):
        project_type = self.project_id.project_type_id
        if not project_type.wip_account_id:
            raise ValidationError(_(
                'The project type {} has no WIP account. '
                'The WIP account must be set on the project type before confirming the '
                'outsourcing purchase order.'
            ).format(project_type.display_name))

    def button_confirm(self):
        outsourcing_orders = self.filtered(lambda o: o.is_outsourcing)
        for order in outsourcing_orders:
            order._check_outsourcing_project_has_type()
            order._check_outsourcing_project_type_has_wip_account()
        return super().button_confirm()


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    is_outsourcing = fields.Boolean(related='order_id.is_outsourcing')

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if line.is_outsourcing:
            line.order_id._propagate_project_to_order_lines()
        return line
