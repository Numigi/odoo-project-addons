# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from .common import AccountCase, AccountMoveCase, InvoiceCase
from odoo.exceptions import ValidationError


class TestInvoiceValidationConstraints(InvoiceCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_2.project_id = cls.project_2

    def test_if_task_on_invoice_line_matches_project__error_not_raised(self):
        assert self.invoice.invoice_line_ids.task_id == self.task
        self._validate_invoice()
        assert self.invoice.state == 'open'

    def test_if_invoice_line_has_project_but_no_task__error_not_raised(self):
        self.invoice.invoice_line_ids.task_id = False
        self._validate_invoice()
        assert self.invoice.state == 'open'

    def test_if_task_on_invoice_line_not_matching_project__raise_error(self):
        self.invoice.invoice_line_ids.task_id = self.task_2

        with pytest.raises(ValidationError):
            self._validate_invoice()

    def test_if_task_on_tax_line_matches_project__error_not_raised(self):
        self.tax.analytic = True
        self.invoice.compute_taxes()
        tax_line = self.invoice.tax_line_ids
        assert tax_line.task_id == self.task
        assert tax_line.account_analytic_id == self.analytic_account
        self._validate_invoice()
        assert self.invoice.state == 'open'

    def test_if_tax_line_has_project_but_no_task__error_not_raised(self):
        self.invoice.invoice_line_ids.task_id = False
        self.tax.analytic = True
        self.invoice.compute_taxes()
        tax_line = self.invoice.tax_line_ids
        assert not tax_line.task_id
        assert tax_line.account_analytic_id == self.analytic_account
        self._validate_invoice()
        assert self.invoice.state == 'open'

    def test_if_task_on_tax_line_not_matching_project__raise_error(self):
        self.tax.analytic = True
        self.invoice.compute_taxes()
        self.invoice.tax_line_ids.task_id = self.task_2
        with pytest.raises(ValidationError):
            self._validate_invoice()

    def test_if_task_has_draft_invoice__changing_project_not_blocked(self):
        self.task.project_id = self.project_2
        self.task.refresh()
        assert self.task.project_id == self.project_2

    def test_if_task_has_open_invoice__changing_project_blocked(self):
        self._validate_invoice()
        with pytest.raises(ValidationError):
            self.task.project_id = self.project_2

    def test_if_task_has_paid_invoice__changing_project_blocked(self):
        self.invoice.state = 'paid'
        with pytest.raises(ValidationError):
            self.task.project_id = self.project_2

    def test_if_is_same_project__changing_project_not_blocked(self):
        self._validate_invoice()
        self.task.project_id = self.task.project_id


class TestAccountMovePostConstraints(AccountMoveCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_2.project_id = cls.project_2

    def test_if_task_matches_project__error_not_raised(self):
        self.move.post()
        assert self.move.state == 'posted'

    def test_if_move_has_project_but_no_task__error_not_raised(self):
        self.debit.task_id = False
        self.move.post()
        assert self.move.state == 'posted'

    def test_if_task_not_matching_project__error_raised(self):
        self.debit.task_id = self.task_2
        with pytest.raises(ValidationError):
            self.move.post()

    def test_if_task_has_draft_move__changing_project_not_blocked(self):
        self.task.project_id = self.project_2
        self.task.refresh()
        assert self.task.project_id == self.project_2

    def test_if_task_has_posted_move__changing_project_blocked(self):
        self.move.post()
        with pytest.raises(ValidationError):
            self.task.project_id = self.project_2


class TestAnalyticLineConstraints(AccountCase):

    def test_after_changing_project__if_task_not_matching_analytic_account__raise_error(self):
        line = self.env['account.analytic.line'].create({
            'name': '/',
            'project_id': self.project.id,
            'task_id': self.task.id,
            'user_id': self.account_user.id,
        })
        with pytest.raises(ValidationError):
            line.project_id = self.project_2

    def test_after_changing_task__if_task_not_matching_analytic_account__raise_error(self):
        line = self.env['account.analytic.line'].create({
            'name': '/',
            'project_id': self.project.id,
            'task_id': self.task.id,
            'user_id': self.account_user.id,
        })
        self.task_2.project_id = self.project_2
        with pytest.raises(ValidationError):
            line.origin_task_id = self.task_2
