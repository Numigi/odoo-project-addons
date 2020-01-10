# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_material.tests.common import TaskMaterialCase


class ProjectWIPMaterialCase(TaskMaterialCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manager.groups_id |= cls.env.ref('account.group_account_manager')

        cls.journal = cls.env['account.journal'].create({
            'name': 'Stock Journal',
            'type': 'general',
            'code': 'STOCK',
            'company_id': cls.company.id,
        })

        cls.stock_account = cls.env['account.account'].create({
            'name': 'Raw Material Stocks',
            'code': '130101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'company_id': cls.company.id,
        })

        cls.input_account = cls.env['account.account'].create({
            'name': 'Stock Received / Not Invoiced',
            'code': '230102',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'company_id': cls.company.id,
        })

        cls.output_account = cls.env['account.account'].create({
            'name': 'Stock Delivered / Not Invoiced',
            'code': '130102',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'company_id': cls.company.id,
        })

        cls.wip_account = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'reconcile': True,
            'company_id': cls.company.id,
        })

        cls.project_type = cls.env['project.type'].create({
            'name': 'Trailer Refurb',
            'wip_account_id': cls.wip_account.id,
        })
        cls.project.project_type_id = cls.project_type

        cls.product_category.write({
            'property_valuation': 'real_time',
            'property_stock_journal': cls.journal.id,
            'property_stock_valuation_account_id': cls.stock_account.id,
            'property_stock_account_input_categ_id': cls.input_account.id,
            'property_stock_account_output_categ_id': cls.output_account.id,
        })

        new_context = dict(cls.env.context, apply_project_wip_material_constraints=True)
        cls.env = cls.env(context=new_context)
