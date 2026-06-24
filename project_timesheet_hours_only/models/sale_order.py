# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('analytic_account_id.line_ids')
    def _compute_timesheet_ids(self):
        # Call the original method to retrieve the standard timesheets.
        super(SaleOrder, self)._compute_timesheet_ids()

        for order in self:
            # Filter the results using the same logic (t.task_id) to keep
            # actual labor hours only and exclude material consumption.
            order.timesheet_ids = order.timesheet_ids.filtered(lambda t: t.task_id)

            # Update the counter displayed on the smart button.
            order.timesheet_count = len(order.timesheet_ids)

            # Note: the 'timesheet_total_duration' field updates by itself
            # since it depends on the 'timesheet_ids' we just filtered.

    def action_view_timesheet(self):
        # Get the action from the original smart button.
        action = super(SaleOrder, self).action_view_timesheet()

        # Restrict the displayed lines to those linked to a task.
        if isinstance(action, dict) and action.get('domain'):
            action['domain'].append(('task_id', '!=', False))

        return action


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_compute_delivered_quantity_domain(self):
        # Apply the same "hours only" logic to the delivered quantity: only
        # analytic lines linked to a task (actual timesheets) are counted,
        # material consumption (task_id == False) is excluded.
        domain = super()._timesheet_compute_delivered_quantity_domain()
        return expression.AND([domain, [('task_id', '!=', False)]])
