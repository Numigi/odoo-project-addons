# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from .common import TestAnalyticLineBase


class TestGenerateInvoice(TestAnalyticLineBase):

    @classmethod
    def setUpClass(cls):
        super(TestGenerateInvoice, cls).setUpClass()
        cls.line_1 = cls.create_analytic_line(4, -120)
        cls.line_2 = cls.create_analytic_line(3, -180)

    def test_01_generate_invoice_real(self):
        lines = [
            {
                'id': self.line_1.id,
                'partner_invoice_id': self.customer.name_get()[0],
                'final_price_currency_id': self.currency.name_get()[0],
                'final_price': 50,
            },
            {
                'id': self.line_2.id,
                'partner_invoice_id': self.customer.name_get()[0],
                'final_price_currency_id': self.currency.name_get()[0],
                'final_price': 70,
            },
        ]
        invoice_ids = self.project.generate_invoices({
            'tasks': {
                self.task.id: {
                    'id': self.task.id,
                    'mode': 'real',
                    'lines': lines,
                    'description': 'My task description',
                }
            },
        })['domain'][0][2]

        self.assertEqual(len(invoice_ids), 1)
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(invoice.amount_total, 50 * 4 + 70 * 3)
        self.assertEqual(invoice.account_id, self.receivable)
        self.assertEqual(self.task.invoiced_amount, invoice.amount_total)

    def test_02_generate_invoice_lump_sum(self):
        lines = [
            {
                'id': self.line_1.id,
                'partner_invoice_id': self.customer.name_get()[0],
            },
            {
                'id': self.line_2.id,
                'partner_invoice_id': self.customer.name_get()[0],
            },
        ]
        invoice_ids = self.project.generate_invoices({
            'tasks': {
                self.task.id: {
                    'id': self.task.id,
                    'currency_id': self.currency.id,
                    'mode': 'lump_sum',
                    'lines': lines,
                    'description': 'My task description',
                    'global_amount': 500,
                }
            },
        })['domain'][0][2]

        self.assertEqual(len(invoice_ids), 1)
        invoice = self.env['account.invoice'].browse(invoice_ids[0])
        self.assertEqual(invoice.amount_total, 500)
        self.assertEqual(invoice.account_id, self.receivable)
        self.assertEqual(self.task.invoiced_amount, invoice.amount_total)
