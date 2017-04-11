# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import api, fields, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    source_analytic_line_ids = fields.One2many(
        'account.analytic.line', 'generated_invoice_id',
        'Source Analytic Lines')

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        self.mapped('source_analytic_line_ids').write({
            'invoicing_state': 'invoiced',
        })
        return res

    @api.multi
    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()
        self.mapped('source_analytic_line_ids').write({
            'invoicing_state': 'to_invoice',
            'generated_invoice_id': False,
        })
        return res
