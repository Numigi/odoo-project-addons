# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from odoo import fields
from odoo.tests import common
from odoo.exceptions import ValidationError


class WIPJournalEntriesCase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({
            'name': 'Test Company',
        })
        cls.manager = cls.env['res.users'].create({
            'name': 'Manager',
            'login': 'manager',
            'email': 'manager@test.com',
            'groups_id': [
                (4, cls.env.ref('project.group_project_manager').id),
            ],
            'company_id': cls.company.id,
            'company_ids': [(4, cls.company.id)],
        })

        cls.timesheet_user = cls.env['res.users'].create({
            'name': 'Timesheet User',
            'login': 'timesheet_user@example.com',
            'email': 'timesheet_user@example.com',
            'groups_id': [
                (4, cls.env.ref('hr_timesheet.group_hr_timesheet_user').id),
            ],
            'company_id': cls.company.id,
            'company_ids': [(4, cls.company.id)],
        })

        cls.employee = cls.env['hr.employee'].create({
            'name': 'Timesheet User',
            'user_id': cls.timesheet_user.id,
        })

        cls.shop_supply_journal = cls.env['account.journal'].create({
            'name': 'Shop Supply To WIP',
            'code': 'SHOP',
            'type': 'general',
            'company_id': cls.company.id,
        })

        cls.cgs_journal = cls.env['account.journal'].create({
            'name': 'Work in Progress',
            'code': 'WIP',
            'update_posted': True,
            'type': 'general',
            'company_id': cls.company.id,
        })

        cls.wip_account = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'reconcile': True,
            'company_id': cls.company.id,
        })

        cls.cgs_account = cls.env['account.account'].create({
            'name': 'Cost of Goods Sold',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
            'company_id': cls.company.id,
        })

        cls.shop_supply_account = cls.env['account.account'].create({
            'name': 'Shop Supply',
            'code': '510201',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
            'company_id': cls.company.id,
        })

        cls.env = cls.env(user=cls.manager, context={'force_company': cls.company.id})

        cls.env['project.project'].create({
            'name': 'Job 123',
            'company_id': cls.company.id,
        })

        cls.shop_supply_rate = 15
        cls.project_type = cls.env['project.type'].create({
            'name': 'Trailer Refurb',
            'wip_account_id': cls.wip_account.id,
            'shop_supply_journal_id': cls.shop_supply_journal.id,
            'shop_supply_account_id': cls.shop_supply_account.id,
            'shop_supply_rate': cls.shop_supply_rate,
            'cgs_account_id': cls.cgs_account.id,
            'cgs_journal_id': cls.cgs_journal.id,
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
            'project_type_id': cls.project_type.id,
            'company_id': cls.company.id,
        })

        cls.task = cls.env['project.task'].create({
            'name': 'Task 450',
            'project_id': cls.project.id,
            'company_id': cls.company.id,
        })

    @classmethod
    def _create_timesheet(cls, description="/", quantity=1, amount=50, date_=None):
        cls.employee.timesheet_cost = amount
        line = cls.env['account.analytic.line'].sudo(cls.timesheet_user).create({
            'company_id': cls.company.id,
            'project_id': cls.project.id,
            'task_id': cls.task.id,
            'employee_id': cls.employee.id,
            'name': description,
            'date': date_ or datetime.now().date(),
            'unit_amount': quantity,
        })
        return line.sudo()


class TestWIPJournalEntries(WIPJournalEntriesCase):

    def test_if_shop_supply_account_filled__shop_supply_journal_must_be_filled(self):
        with pytest.raises(ValidationError):
            self.project_type.shop_supply_journal_id = False

    def test_if_shop_supply_account_filled__wip_account_must_be_filled(self):
        with pytest.raises(ValidationError):
            self.project_type.wip_account_id = False

    def test_on_create_timesheet__account_move_created(self):
        timesheet_line = self._create_timesheet()
        assert timesheet_line.shop_supply_account_move_id

    def test_on_create_timesheet__account_move_is_posted(self):
        timesheet_line = self._create_timesheet()
        assert timesheet_line.shop_supply_account_move_id.state == 'posted'

    def test_after_timesheet_write__account_move_is_posted(self):
        timesheet_line = self._create_timesheet()
        timesheet_line.unit_amount = -100
        assert timesheet_line.shop_supply_account_move_id.state == 'posted'

    def test_account_move_has_analytic_lines(self):
        timesheet_line = self._create_timesheet()
        shop_supply_move = timesheet_line.shop_supply_account_move_id
        assert shop_supply_move.mapped('line_ids.analytic_line_ids')

    def _get_wip_move_line(self, timesheet_line):
        return timesheet_line.shop_supply_account_move_id.line_ids.filtered(
            lambda l: l.account_id == self.wip_account)

    def _get_shop_supply_move_line(self, timesheet_line):
        return timesheet_line.shop_supply_account_move_id.line_ids.filtered(
            lambda l: l.account_id == self.shop_supply_account)

    def test_wip_move_line_analytic_account_is_project(self):
        timesheet_line = self._create_timesheet()
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.analytic_account_id == self.project.analytic_account_id

    def test_wip_move_line_task_is_set(self):
        timesheet_line = self._create_timesheet()
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.task_id == self.task

    def test_wip_move_line_with_positive_timesheet__has_debit(self):
        quantity = 2
        expected_amount = 30  # 2 * 15 (quantity * shop supply rate)
        timesheet_line = self._create_timesheet(quantity=quantity)
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.debit == expected_amount

    def test_wip_move_line_with_negative_timesheet__has_credit(self):
        quantity = -2
        expected_amount = 30  # -2 * 15 (quantity * shop supply rate)
        timesheet_line = self._create_timesheet(quantity=quantity)
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.credit == expected_amount

    def test_shop_supply_move_line_has_no_analytic_account(self):
        timesheet_line = self._create_timesheet()
        shop_supply_line = self._get_shop_supply_move_line(timesheet_line)
        assert shop_supply_line
        assert not shop_supply_line.analytic_account_id

    def test_shop_supply_move_line_has_no_task(self):
        timesheet_line = self._create_timesheet()
        shop_supply_line = self._get_shop_supply_move_line(timesheet_line)
        assert shop_supply_line
        assert not shop_supply_line.task_id

    def test_on_change_timesheet_quantity__move_quantity_updated(self):
        timesheet_line = self._create_timesheet()
        expected_quantity = 5
        timesheet_line.sudo(self.timesheet_user).unit_amount = expected_quantity
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.quantity == expected_quantity

    def test_on_change_timesheet_a_date__account_move_date_updated(self):
        timesheet_line = self._create_timesheet()
        new_date = fields.Date.to_string(datetime.now().date() + timedelta(30))
        timesheet_line.sudo(self.timesheet_user).date = new_date
        assert timesheet_line.shop_supply_account_move_id.date == new_date

    def test_if_project_has_no_type__no_account_move_created(self):
        self.project.project_type_id = False
        timesheet_line = self._create_timesheet()
        assert not timesheet_line.shop_supply_account_move_id

    def test_if_project_type_has_no_shop_supply_account__no_account_move_created(self):
        self.project_type.shop_supply_account_id = False
        timesheet_line = self._create_timesheet()
        assert not timesheet_line.shop_supply_account_move_id

    def test_if_timesheet_deleted__account_move_reversed(self):
        timesheet_line = self._create_timesheet()
        wip_line = self._get_wip_move_line(timesheet_line)
        timesheet_line.unlink()
        assert wip_line.reconciled

    def test_reversal_move_wip_line_has_task(self):
        timesheet_line = self._create_timesheet()
        wip_line = self._get_wip_move_line(timesheet_line)
        timesheet_line.unlink()
        assert wip_line.matched_credit_ids.credit_move_id.task_id == self.task

    def test_if_new_project_requires_no_timesheet__account_move_reversed(self):
        timesheet_line = self._create_timesheet()
        new_project = self.project.copy({'project_type_id': False})
        new_task = self.task.copy({'project_id': new_project.id})

        wip_line = self._get_wip_move_line(timesheet_line)
        timesheet_line.sudo(self.timesheet_user).write({
            'project_id': new_project.id,
            'task_id': new_task.id,
        })
        assert wip_line.reconciled

    def test_timesheet_unit_amount_can_be_changed_twice(self):
        timesheet_line = self._create_timesheet()
        expected_quantity = 5
        timesheet_line.sudo(self.timesheet_user).unit_amount = 99
        timesheet_line.sudo(self.timesheet_user).unit_amount = expected_quantity
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.quantity == expected_quantity

    def test_move_ref_contains_task_id(self):
        timesheet_line = self._create_timesheet()
        assert str(self.task.id) in timesheet_line.shop_supply_account_move_id.ref

    def test_after_change_task_on_timesheet__move_ref_contains_task_id(self):
        timesheet_line = self._create_timesheet()
        new_task = self.task.copy()
        timesheet_line.sudo(self.timesheet_user).task_id = new_task
        assert str(new_task.id) in timesheet_line.shop_supply_account_move_id.ref

    def test_move_ref_contains_project_name(self):
        timesheet_line = self._create_timesheet()
        assert self.project.name in timesheet_line.shop_supply_account_move_id.ref

    def test_after_change_project_on_timesheet__move_ref_contains_project_name(self):
        timesheet_line = self._create_timesheet()
        new_project = self.project.copy()
        new_task = self.task.copy({'project_id': new_project.id})
        timesheet_line.sudo(self.timesheet_user).write({
            'project_id': new_project.id,
            'task_id': new_task.id,
        })
        assert new_project.name in timesheet_line.shop_supply_account_move_id.ref


class TestTimesheetEntryTransferedToWip(WIPJournalEntriesCase):
    """Test the cases where the WIP entries are already transfered to CGS."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.timesheet_line = cls._create_timesheet()
        cls.project.sudo().action_wip_to_cgs()

    def test_timesheet_quantity_can_not_be_changed(self):
        with pytest.raises(ValidationError):
            self.timesheet_line.sudo(self.timesheet_user).unit_amount = 10

    def test_project_with_no_type_can_not_be_set(self):
        new_project = self.project.copy({'project_type_id': False})
        new_task = self.task.copy({'project_id': new_project.id})
        with pytest.raises(ValidationError):
            self.timesheet_line.sudo(self.timesheet_user).write({
                'project_id': new_project.id,
                'task_id': new_task.id,
            })

    def test_timesheet_can_not_be_deleted(self):
        with pytest.raises(ValidationError):
            self.timesheet_line.sudo(self.timesheet_user).unlink()
