# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    """Select the task and analytic account on invoice lines for outsourcing."""

    _inherit = 'account.invoice'

    def _prepare_invoice_line_from_po_line(self, line):
        result = super()._prepare_invoice_line_from_po_line(line)
        if line.is_outsourcing:
            project = line.order_id.project_id
            result['account_analytic_id'] = project.analytic_account_id.id
            result['task_id'] = line.order_id.task_id.id
        return result


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    is_outsourcing = fields.Boolean(related='purchase_id.is_outsourcing')

    def _get_outsourcing_analytic_account(self):
        return self.purchase_id.project_id.analytic_account_id

    def _get_outsourcing_task(self):
        return self.purchase_id.task_id

    @api.onchange('product_id')
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        if self.is_outsourcing:
            self.account_analytic_id = self._get_outsourcing_analytic_account()
            self.task_id = self._get_outsourcing_task()
        return result
