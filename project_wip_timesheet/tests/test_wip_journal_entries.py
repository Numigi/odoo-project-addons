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
        })

        cls.salary_account = cls.env['account.account'].create({
            'name': 'Salary',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
            'company_id': cls.company.id,
        })

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

    def _create_timesheet(self, description="/", quantity=1, amount=50, date_=None):
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
        line = self._create_timesheet()
        assert line.salary_account_move_id
