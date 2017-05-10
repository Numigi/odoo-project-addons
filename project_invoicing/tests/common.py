# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from datetime import datetime
from odoo.tests import common


class TestAnalyticLineBase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticLineBase, cls).setUpClass()
        cls.currency = cls.env.ref('base.CAD')
        cls.company = cls.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': cls.currency.id,
        })
        cls.env['account.journal'].create({
            'name': 'Sales Journal (CAD)',
            'type': 'sale',
            'code': 'SALE_CAD',
            'company_id': cls.company.id,
            'currency_id': cls.currency.id,
        })
        cls.receivable = cls.env['account.account'].create({
            'company_id': cls.company.id,
            'name': 'Account Receivable',
            'code': '100001',
            'user_type_id': cls.env.ref(
                'account.data_account_type_receivable').id,
            'reconcile': True,
        })
        cls.income = cls.env['account.account'].create({
            'company_id': cls.company.id,
            'name': 'Income',
            'code': '600001',
            'user_type_id': cls.env.ref(
                'account.data_account_type_revenue').id,
        })

        cls.company.property_account_income_id = cls.income

        cls.set_default_property(
            'product.template', 'property_account_income_id',
            cls.income)

        cls.set_default_property(
            'res.partner', 'property_account_receivable_id',
            cls.receivable)

        cls.journal = cls.env['account.journal'].create({
            'company_id': cls.company.id,
            'type': 'sale',
            'name': 'Sale Journal',
            'code': 'SAJ',
        })

        cls.customer = cls.env['res.partner'].create({
            'name': 'My Partner',
            'customer': True,
            'property_account_receivable_id': cls.receivable.id,
        })
        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
            'partner_id': cls.customer.id,
            'company_id': cls.company.id,
        })
        cls.task = cls.env['project.task'].create({
            'name': 'My Task',
            'project_id': cls.project.id,
            'company_id': cls.company.id,
        })
        cls.user = cls.env['res.users'].create({
            'name': 'My User',
            'login': 'test_project_invoicing',
            'email': 'root@localhost',
            'groups_id': [(6, 0, [(cls.env.ref('base.group_user')).id])]
        })
        cls.product_service = cls.env['product.product'].create({
            'name': 'My Service',
            'type': 'service',
            'standard_price': 40,
        })
        cls.employee = cls.env['hr.employee'].create({
            'name': 'My Employee',
            'user_id': cls.user.id,
            'product_id': cls.product_service.id,
        })
        cls.product = cls.env['product.product'].create({
            'name': 'My Product',
            'type': 'product',
        })

    @classmethod
    def set_default_property(cls, model, name, obj):
        field = cls.env['ir.model.fields'].search([
            ('model', '=', model),
            ('name', '=', name),
        ], limit=1)
        cls.env['ir.property'].create({
            'name': name,
            'company_id': cls.company.id,
            'value_reference': '%s,%s' % (obj._name, obj.id),
            'fields_id': field.id,
        })

    @classmethod
    def create_analytic_line(cls, quantity, amount):
        return cls.env['account.analytic.line'].create({
            'name': '/',
            'date': datetime.now(),
            'user_id': cls.user.id,
            'project_id': cls.project.id,
            'task_id': cls.task.id,
            'product_id': cls.product.id,
            'amount': amount,
            'unit_amount': quantity,
        })

    @classmethod
    def create_timesheet_line(cls, hours):
        return cls.env['account.analytic.line'].create({
            'name': '/',
            'date': datetime.now(),
            'user_id': cls.user.id,
            'project_id': cls.project.id,
            'task_id': cls.task.id,
            'amount': -hours * 40,
            'unit_amount': hours,
            'is_timesheet': True,
        })
