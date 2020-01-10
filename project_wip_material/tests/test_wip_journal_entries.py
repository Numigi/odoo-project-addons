# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
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


class TestConsumptionJournalEntryConstraints(ProjectWIPMaterialCase):

    def test_if_project_has_no_type__constraint_raised_on_task_material(self):
        self.project.project_type_id = False
        with pytest.raises(ValidationError):
            self._create_material_line()

    def test_if_project_type_has_no_wip_account__constraint_raised_on_task_material(self):
        self.project_type.wip_account_id = False
        with pytest.raises(ValidationError):
            self._create_material_line()

    def test_if_project_has_no_type__constraint_raised_on_transfer(self):
        self.move = self._create_material_line().move_ids
        self.project.project_type_id = False
        with pytest.raises(ValidationError):
            self._force_transfer_move(self.move)

    def test_if_project_type_has_no_wip_account__constraint_raised_on_transfer(self):
        self.move = self._create_material_line().move_ids
        self.project_type.wip_account_id = False
        with pytest.raises(ValidationError):
            self._force_transfer_move(self.move)


class TestConsumptionJournalEntry(ProjectWIPMaterialCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.move = cls._create_material_line(initial_qty=10).move_ids
        cls._force_transfer_move(cls.move)
        cls.account_move = cls.move.account_move_ids
        cls.debit_line = cls.account_move.line_ids.filtered(lambda l: l.debit)
        cls.credit_line = cls.account_move.line_ids.filtered(lambda l: l.credit)
        cls.expected_value = 500  # 50 * 10 (product_a_value * initial_qty)

    def test_debit_account_is_wip(self):
        assert self.debit_line.account_id == self.wip_account

    def test_credit_account_is_inventory_valuation(self):
        assert self.credit_line.account_id == self.stock_account

    def test_debit_analytic_account_is_project(self):
        assert self.debit_line.analytic_account_id == self.project.analytic_account_id

    def test_debit_task_is_set(self):
        assert self.debit_line.task_id == self.task

    def test_credit_has_no_analytic_account(self):
        assert not self.credit_line.analytic_account_id

    def test_credit_has_no_task(self):
        assert not self.credit_line.task_id

    def test_product_propagated_to_account_move(self):
        assert self.debit_line.product_id == self.product_a
        assert self.credit_line.product_id == self.product_a

    def test_move_line_ref_is_picking_name(self):
        assert self.debit_line.ref == self.move.picking_id.name
        assert self.credit_line.ref == self.move.picking_id.name

    def test_one_analytic_line_created_for_debit(self):
        assert len(self.debit_line.analytic_line_ids) == 1

    def test_anayltic_line_has_origin_task(self):
        assert self.debit_line.analytic_line_ids.origin_task_id == self.task

    def test_no_analytic_line_created_for_credit(self):
        assert not self.credit_line.analytic_line_ids

    def test_one_analytic_amount_is_move_value(self):
        assert self.debit_line.analytic_line_ids.amount == -self.expected_value


class TestConsumptionReturnJournalEntry(ProjectWIPMaterialCase):
    """Test the journal entry generated from a consumption return.

    The expected behavior is the opposite from a consumption journal entry.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        initial_move = cls._create_material_line(initial_qty=10).move_ids
        cls._force_transfer_move(initial_move)
        cls.move = cls._return_stock_move(initial_move, 10)
        cls.account_move = cls.move.account_move_ids
        cls.debit_line = cls.account_move.line_ids.filtered(lambda l: l.debit)
        cls.credit_line = cls.account_move.line_ids.filtered(lambda l: l.credit)
        cls.expected_value = 500  # 50 * 10 (product_a_value * initial_qty)

    def test_credit_account_is_wip(self):
        assert self.credit_line.account_id == self.wip_account

    def test_debit_account_is_inventory_valuation(self):
        assert self.debit_line.account_id == self.stock_account

    def test_credit_analytic_account_is_project(self):
        assert self.credit_line.analytic_account_id == self.project.analytic_account_id

    def test_credit_task_is_set(self):
        assert self.credit_line.task_id == self.task

    def test_debit_has_no_analytic_account(self):
        assert not self.debit_line.analytic_account_id

    def test_debit_has_no_task(self):
        assert not self.debit_line.task_id

    def test_product_propagated_to_account_move(self):
        assert self.credit_line.product_id == self.product_a
        assert self.debit_line.product_id == self.product_a

    def test_move_line_ref_is_picking_name(self):
        assert self.credit_line.ref == self.move.picking_id.name
        assert self.debit_line.ref == self.move.picking_id.name

    def test_one_analytic_line_created_for_credit(self):
        assert len(self.credit_line.analytic_line_ids) == 1

    def test_anayltic_line_has_origin_task(self):
        assert self.credit_line.analytic_line_ids.origin_task_id == self.task

    def test_no_analytic_line_created_for_debit(self):
        assert not self.debit_line.analytic_line_ids

    def test_one_analytic_amount_is_move_value(self):
        assert self.credit_line.analytic_line_ids.amount == self.expected_value
