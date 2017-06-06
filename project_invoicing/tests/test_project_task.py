# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo.tests import common


class TestProjectTask (common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectTask, cls).setUpClass()

        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
        })

        cls.task = cls.env['project.task'].create({
            'name': 'My Task',
            'project_id': cls.project.id,
        })

        cls.supplier = cls.env['res.partner'].create({
            'name': 'My Supplier',
            'is_company': True,
        })

        cls.account = cls.env['account.account'].create({
            'code': '123456',
            'name': 'My Account',
            'user_type_id': cls.env.ref(
                'account.data_account_type_expenses').id,
        })

        cls.invoice_1 = cls.env['account.invoice'].create({
            'partner_id': cls.supplier.id,
            'account_analytic_id': cls.project.analytic_account_id.id,
            'type': 'in_invoice',
        })
        cls.invoice_line_1 = cls.env['account.invoice.line'].create({
            'invoice_id': cls.invoice_1.id,
            'name': 'My line 1',
            'account_id': cls.account.id,
            'price_unit': '5000',
        })

        cls.invoice_2 = cls.env['account.invoice'].create({
            'partner_id': cls.supplier.id,
            'account_analytic_id': cls.project.analytic_account_id.id,
            'type': 'out_invoice',
        })
        cls.invoice_line_2 = cls.env['account.invoice.line'].create({
            'invoice_id': cls.invoice_2.id,
            'name': 'My line 2',
            'account_id': cls.account.id,
            'price_unit': '6000',
        })

    def test_01_customer_invoice_list(self):
        self.task.write({
            'invoice_line_ids': [
                (4, self.invoice_line_1.id), (4, self.invoice_line_2.id)]
        })
        view = self.task.get_invoice_list_action()
        self.assertEquals(view['domain'][0][2], [self.invoice_2.id])

    def test_02_invoiced_amount(self):
        self.task.write({
            'invoice_line_ids': [
                (4, self.invoice_line_1.id), (4, self.invoice_line_2.id)]
        })
        self.assertEquals(self.task.invoiced_amount, 6000)
