# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestAccountInvoice(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoice, cls).setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'My Company',
            'is_company': True,
        })

        cls.currency = cls.env['res.currency'].search(
            [('name', '=', 'EUR')]
        )

        cls.project = cls.env['project.project'].create({
            'name': 'My Test Project',
        })

        cls.task = cls.env['project.task'].create({
            'name': 'My Task',
            'project_id': cls.project.id,
        })

        cls.account_invoice = cls.env['account.invoice'].create({
            'partner_id': cls.supplier.id,
            'currency_id': cls.currency.id,
            'account_analytic_id': cls.project.analytic_account_id.id,
        })

        cls.account = cls.env['account.account'].create({
            'code': '123456',
            'name': 'My account',
            'user_type_id': cls.env.ref(
                'account.data_account_type_expenses').id,
        })

        cls.account_invoice_line = cls.env['account.invoice.line'].create({
            'name': 'My line',
            'account_id': cls.account.id,
            'price_unit': '20',
        })

    def test_01_invoice_line_with_wrong_task(self):
        new_project = self.env['project.project'].create({
            'name': 'New Project',
        })
        new_task = self.env['project.task'].create({
            'name': 'New Task',
            'project_id': new_project.id,
        })

        with self.assertRaises(ValidationError):
            self.account_invoice_line.write({
                'account_analytic_id': self.project.analytic_account_id.id,
                'task_id': new_task.id,
            })

    def test_02_invoice_line_with_correct_task(self):
        self.account_invoice_line.write({
            'account_analytic_id': self.project.analytic_account_id.id,
            'task_id': self.task.id,
        })
