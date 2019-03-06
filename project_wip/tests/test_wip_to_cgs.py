# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestWIPTrasferToCGS(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_journal = cls.env['account.journal'].create({
            'name': 'MRP / Production',
            'code': 'MRP',
            'update_posted': True,
            'type': 'general',
        })
        cls.wip_journal = cls.env['account.journal'].create({
            'name': 'Work in Progress',
            'code': 'WIP',
            'update_posted': True,
            'type': 'general',
        })

        cls.stock_account = cls.env['account.account'].create({
            'name': 'Raw Material Stocks',
            'code': '130101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
        })
        cls.cgs_account = cls.env['account.account'].create({
            'name': 'Cost of Goods Sold',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
        })
        cls.wip_account = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
        })

        cls.partner = cls.env['res.partner'].create({
            'name': 'Customer',
            'customer': True,
        })

        cls.product_raw = cls.env['product.product'].create({
            'name': 'Raw Material',
            'type': 'product',
        })

        cls.project_type = cls.env['project.type'].create({
            'name': 'Trailer Refurb',
            'wip_journal_id': cls.wip_journal.id,
            'wip_account_id': cls.wip_account.id,
            'cgs_account_id': cls.cgs_account.id,
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
            'partner_id': cls.partner.id,
            'type_id': cls.project_type.id,
        })

        cls.raw_material_move = cls.env['account.move'].create({
            'journal_id': cls.journal.id,
            'line_ids': [
                (0, 0, {
                    'name': 'Consume Raw Materials',
                    'account_id': cls.wip_account.id,
                    'analytic_account_id': cls.analytic_account.id,
                    'partner_id': cls.partner.id,
                    'product_id': cls.product_raw.id,
                    'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
                    'debit': 100,
                }),
                (0, 0, {
                    'name': 'Consume Raw Materials',
                    'account_id': cls.stock_account.id,
                    'product_id': cls.product_raw.id,
                    'product_uom_id': cls.env.ref('uom.product_uom_unit').id,
                    'credit': 100,
                }),
            ],
        })
        cls.wip_line = cls.raw_material_move.line_ids.filtered(
            lambda l: l.account_id == cls.wip_account)
        cls.raw_material_move.post()

    def test_after_process__wip_line_reconciled(self):
        assert not self.wip_line.reconciled
        self.project.action_wip_to_cgs()
        assert self.wip_line.reconciled
