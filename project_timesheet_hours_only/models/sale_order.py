# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('analytic_account_id.line_ids')
    def _compute_timesheet_ids(self):
        super(SaleOrder, self)._compute_timesheet_ids()
        for order in self:
            order.timesheet_ids = order.timesheet_ids.filtered(
                lambda t: t.task_id and t.project_id in order.project_ids
            )
            order.timesheet_count = len(order.timesheet_ids)

    def action_view_timesheet(self):
        action = super(SaleOrder, self).action_view_timesheet()
        # Restrict the displayed lines to those linked to a task.
        if isinstance(action, dict) and action.get('domain'):
            action['domain'].append(('task_id', '!=', False))
            action['domain'].append(('project_id', 'in', self.project_ids.ids))

        return action


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_compute_delivered_quantity_domain(self):
        # Apply the same "hours only" logic to the delivered quantity: only
        # analytic lines linked to a task (actual timesheets) are counted,
        # material consumption (task_id == False) is excluded.
        domain = super()._timesheet_compute_delivered_quantity_domain()
        return expression.AND([domain, [('task_id', '!=', False)]])
