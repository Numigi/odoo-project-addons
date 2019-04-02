# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):

    _inherit = 'project.task'

    def _check_no_confirmed_outsourcing_to_update(self):
        confirmed_orders = self.outsourcing_po_ids.filtered(
            lambda o: o.state in ('purchase', 'done'))
        orders_to_update = confirmed_orders.filtered(
            lambda o: o.project_id != self.project_id)
        if orders_to_update:
            raise ValidationError(_(
                "The project can not be changed on the task {task}. "
                "The task is linked to the following confirmed outsourcing "
                "purchase orders: {orders}"
            ).format(
                task=self.display_name,
                orders=', '.join(orders_to_update.mapped('display_name')),
            ))

    def _propagate_project_to_outsourcing_orders(self):
        orders_to_update = self.outsourcing_po_ids.filtered(
            lambda o: o.project_id != self.project_id)
        orders_to_update.write({
            'project_id': self.project_id.id,
        })
        orders_to_update.order_line.write({
            'account_analytic_id': self.project_id.analytic_account_id.id,
        })

    @api.multi
    def write(self, vals):
        super().write(vals)
        if 'project_id' in vals:
            for task in self:
                task.sudo()._check_no_confirmed_outsourcing_to_update()
                task.sudo()._propagate_project_to_outsourcing_orders()
        return True
