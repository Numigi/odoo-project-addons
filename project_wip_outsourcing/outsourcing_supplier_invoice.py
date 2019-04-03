# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    """Select the WIP account on invoice lines for outsourcing.

    If the invoice line is linked to an outsourcing PO line,
    the WIP account is automatically selected.

    The WIP account is taken from the project type.
    """

    _inherit = 'account.invoice'

    def _prepare_invoice_line_from_po_line(self, line):
        result = super()._prepare_invoice_line_from_po_line(line)
        if line.is_outsourcing:
            project = line.order_id.project_id
            result['account_id'] = project.project_type_id.wip_account_id.id
            result['account_analytic_id'] = project.analytic_account_id.id
        return result


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    is_outsourcing = fields.Boolean(related='purchase_id.is_outsourcing')

    def _get_outsourcing_wip_account(self):
        return self.purchase_id.project_id.project_type_id.wip_account_id

    def _get_outsourcing_analytic_account(self):
        return self.purchase_id.project_id.analytic_account_id

    @api.onchange('product_id')
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        if self.is_outsourcing:
            self.account_id = self._get_outsourcing_wip_account()
            self.account_analytic_id = self._get_outsourcing_analytic_account()
        return result
