# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime, timedelta
from odoo import fields
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestWIPJournalEntries(common.SavepointCase):

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
            'group_id': [
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

        cls.salary_journal = cls.env['account.journal'].create({
            'name': 'Salary To WIP',
            'code': 'SALARY',
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

        cls.salary_account = cls.env['account.account'].create({
            'name': 'Salary',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
            'company_id': cls.company.id,
        })

        cls.env = cls.env(user=cls.manager, context={'force_company': cls.company.id})

        cls.env['project.project'].create({
            'name': 'Job 123',
            'company_id': cls.company.id,
        })

        cls.project_type = cls.env['project.type'].create({
            'name': 'Trailer Refurb',
            'wip_account_id': cls.wip_account.id,
            'salary_journal_id': cls.salary_journal.id,
            'salary_account_id': cls.salary_account.id,
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

    def _create_timesheet(self, description="/", quantity=1, amount=-50, date_=None):
        line = self.env['account.analytic.line'].sudo(self.timesheet_user).create({
            'company_id': self.company.id,
            'project_id': self.project.id,
            'task_id': self.task.id,
            'user_id': self.timesheet_user.id,
            'name': description,
            'date': date_ or datetime.now().date(),
            'quantity': quantity,
            'amount': amount,
        })
        return line.sudo()

    def test_on_create_timesheet__account_move_created(self):
        timesheet_line = self._create_timesheet()
        assert timesheet_line.salary_account_move_id

    def test_account_move_has_no_analytic_lines(self):
        timesheet_line = self._create_timesheet()
        assert not timesheet_line.salary_account_move_id.mapped('line_ids.analytic_line_ids')

    def _get_wip_move_line(self, timesheet_line):
        return timesheet_line.salary_account_move_id.line_ids.filtered(
            lambda l: l.account_id == self.wip_account)

    def _get_salary_move_line(self, timesheet_line):
        return timesheet_line.salary_account_move_id.line_ids.filtered(
            lambda l: l.account_id == self.salary_account)

    def test_wip_move_line_analytic_account_is_project(self):
        timesheet_line = self._create_timesheet()
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.analytic_account_id == self.project.analytic_account_id

    def test_wip_move_line_with_positive_timesheet__has_debit(self):
        expected_amount = 100
        timesheet_line = self._create_timesheet(amount=-expected_amount)
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.debit == expected_amount

    def test_wip_move_line_with_negative_timesheet__has_credit(self):
        expected_amount = 100
        timesheet_line = self._create_timesheet(quantity=-1, amount=expected_amount)
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.credit == expected_amount

    def test_salary_move_line_has_no_analytic_account(self):
        timesheet_line = self._create_timesheet()
        salary_line = self._get_salary_move_line(timesheet_line)
        assert salary_line
        assert not salary_line.analytic_account_id

    def test_on_change_timesheet_amount__debit_amount_updated(self):
        timesheet_line = self._create_timesheet()
        expected_amount = 25
        timesheet_line.sudo(self.timesheet_user).amount = -expected_amount
        wip_line = self._get_wip_move_line(timesheet_line)
        assert wip_line.debit == expected_amount

    def test_on_change_timesheet_a_date__account_move_date_updated(self):
        timesheet_line = self._create_timesheet()
        new_date = fields.Date.to_string(datetime.now().date() + timedelta(30))
        timesheet_line.sudo(self.timesheet_user).date = new_date
        assert timesheet_line.salary_account_move_id.date == new_date

    def test_if_project_has_no_type__no_account_move_created(self):
        self.project.project_type_id = False
        timesheet_line = self._create_timesheet()
        assert not timesheet_line.salary_account_move_id

    def test_if_project_type_has_no_salary_account__no_account_move_created(self):
        self.project_type.salary_account_id = False
        timesheet_line = self._create_timesheet()
        assert not timesheet_line.salary_account_move_id
