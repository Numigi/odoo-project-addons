# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from freezegun import freeze_time
from datetime import datetime, timedelta
from odoo import fields
from odoo.tests import common
from odoo.exceptions import ValidationError, AccessError


class TestWIPTrasferToCGS(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref("base.user_demo")
        cls.user.groups_id = cls.env.ref("project.group_project_manager")

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
            'reconcile': True,
        })

        cls.partner = cls.env['res.partner'].create({
            'name': 'Customer',
            'customer': True,
        })

        cls.uom = cls.env.ref('product.product_uom_lb')

        cls.product_raw = cls.env['product.product'].create({
            'name': 'Raw Material',
            'type': 'product',
            'uom_id': cls.uom.id,
            'uom_po_id': cls.uom.id,
        })

        cls.project_type = cls.env['project.type'].create({
            'name': 'Trailer Refurb',
            'cgs_journal_id': cls.wip_journal.id,
            'wip_account_id': cls.wip_account.id,
            'cgs_account_id': cls.cgs_account.id,
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
            'partner_id': cls.partner.id,
            'project_type_id': cls.project_type.id,
        })
        cls.analytic_account = cls.project.analytic_account_id

        cls.raw_material_amount = 100
        cls.raw_material_quantity = 10

        cls.raw_material_move = cls.env['account.move'].create({
            'journal_id': cls.wip_journal.id,
            'line_ids': [
                (0, 0, {
                    'name': 'Consume Raw Materials',
                    'account_id': cls.wip_account.id,
                    'analytic_account_id': cls.analytic_account.id,
                    'partner_id': cls.partner.id,
                    'product_id': cls.product_raw.id,
                    'quantity': cls.raw_material_quantity,
                    'product_uom_id': cls.uom.id,
                    'debit': cls.raw_material_amount,
                }),
                (0, 0, {
                    'name': 'Consume Raw Materials',
                    'account_id': cls.stock_account.id,
                    'product_id': cls.product_raw.id,
                    'product_uom_id': cls.uom.id,
                    'quantity': cls.raw_material_quantity,
                    'credit': cls.raw_material_amount,
                }),
            ],
        })
        cls.wip_line = cls.raw_material_move.line_ids.filtered(
            lambda l: l.account_id == cls.wip_account)
        cls.raw_material_move.post()

    def test_after_process__wip_line_reconciled(self):
        assert not self.wip_line.reconciled
        self._action_wip_to_cgs()
        assert self.wip_line.reconciled

    def test_if_wip_line_partially_reconciled__raise_validation_error(self):
        move = self.env['account.move'].create({
            'journal_id': self.wip_journal.id,
            'line_ids': [
                (0, 0, {
                    'account_id': self.stock_account.id,
                    'debit': 50,
                }),
                (0, 0, {
                    'account_id': self.wip_account.id,
                    'credit': 50,
                }),
            ],
        })
        wip_line_2 = move.line_ids.filtered(lambda l: l.account_id == self.wip_account)
        (self.wip_line | wip_line_2).auto_reconcile_lines()

        with pytest.raises(ValidationError):
            self._action_wip_to_cgs()

    def _find_wip_to_cgs_move(self):
        return self.env['account.move'].search([
            ('line_ids.analytic_account_id', '=', self.analytic_account.id),
            ('line_ids.account_id', '=', self.cgs_account.id),
        ])

    def _find_cgs_move_line(self):
        return self.env['account.move.line'].search([
            ('analytic_account_id', '=', self.analytic_account.id),
            ('account_id', '=', self.cgs_account.id),
        ])

    def _action_wip_to_cgs(self):
        self.project.sudo(self.user).action_wip_to_cgs()

    def test_transfer_move_has_no_analytic_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert not transfer_move.mapped('line_ids.analytic_line_ids')

    def test_cgs_move_line_has_expected_amount_in_debit(self):
        self._action_wip_to_cgs()
        cgs_move_line = self._find_cgs_move_line()
        assert cgs_move_line.debit == self.raw_material_amount

    def test_product_propagated_to_transfer_move_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.line_ids[0].product_id == self.product_raw
        assert transfer_move.line_ids[1].product_id == self.product_raw

    def test_product_uom_propagated_to_transfer_move_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.line_ids[0].product_uom_id == self.uom
        assert transfer_move.line_ids[1].product_uom_id == self.uom

    def test_quantity_propagated_to_transfer_move_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.line_ids[0].quantity == self.raw_material_quantity
        assert transfer_move.line_ids[1].quantity == self.raw_material_quantity

    def test_partner_propagated_to_transfer_move_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.line_ids[0].partner_id == self.partner
        assert transfer_move.line_ids[1].partner_id == self.partner

    def test_analytic_account_propagated_to_transfer_move_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.line_ids[0].analytic_account_id == self.analytic_account
        assert transfer_move.line_ids[1].analytic_account_id == self.analytic_account

    def test_move_line_name_propagated_to_transfer_move_lines(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.line_ids[0].name == self.wip_line.name
        assert transfer_move.line_ids[1].name == self.wip_line.name

    def test_after_process__transfer_move_is_posted(self):
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.state == 'posted'

    def test_if_no_specific_date__current_date_is_used(self):
        now = datetime(2020, 4, 13)
        with freeze_time(now):
            self._action_wip_to_cgs()
            transfer_move = self._find_wip_to_cgs_move()
            assert transfer_move.date == fields.Date.to_string(now)

    def test_if_specific_date_given__specific_date_is_used(self):
        specific_date = datetime.now().date() + timedelta(30)
        self.project.action_wip_to_cgs(specific_date)
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.date == fields.Date.to_string(specific_date)

    def test_if_action_ran_twice__only_one_transfer_move_generated(self):
        self._action_wip_to_cgs()
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert len(transfer_move) == 1

    def test_if_2_wip_entries__2_transfer_moves_generated(self):
        raw_move_2 = self.raw_material_move.copy()
        raw_move_2.post()
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert len(transfer_move) == 2

    def test_if_wip_entry_not_posted__no_transfer_move_generated(self):
        self.raw_material_move.copy()
        self._action_wip_to_cgs()
        transfer_move = self._find_wip_to_cgs_move()
        assert len(transfer_move) == 1

    def test_wip_to_cgs_wizard__costs_to_transfer(self):
        wizard = self.env['project.wip.transfer'].create({
            'project_id': self.project.id,
        })
        wizard._onchange_project_compute_costs_to_transfer()
        assert wizard.costs_to_transfer == self.raw_material_amount

    def test_wip_to_cgs_wizard_date_propagated_to_account_move(self):
        specific_date = datetime.now().date() + timedelta(30)
        wizard = self.env['project.wip.transfer'].create({
            'project_id': self.project.id,
            'accounting_date': specific_date,
        })
        wizard.validate()
        transfer_move = self._find_wip_to_cgs_move()
        assert transfer_move.date == fields.Date.to_string(specific_date)

    def test_if_not_project_manager__can_not_transfer_wip_to_cgs(self):
        self.user.groups_id -= self.env.ref("project.group_project_manager")
        with pytest.raises(AccessError):
            self._action_wip_to_cgs()
