# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestJournalEntryPropagation(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.env['account.journal'].search([], limit=1)

        cls.analytic_account = cls.env['account.analytic.account'].create({
            'name': 'Job 123',
        })
        cls.expense = cls.env['account.account'].create({
            'name': 'Expense',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
        })
        cls.revenue = cls.env['account.account'].create({
            'name': 'Revenue',
            'code': '410101',
            'user_type_id': cls.env.ref(
                'account.data_account_type_revenue').id,
        })
        cls.asset = cls.env['account.account'].create({
            'name': 'Asset',
            'code': '110101',
            'user_type_id': cls.env.ref(
                'account.data_account_type_current_assets').id,
        })

        cls.move_1 = cls.env['account.move'].create({
            'journal_id': cls.journal.id,
            'line_ids': [
                (0, 0, {
                    'account_id': cls.expense.id,
                    'analytic_account_id': cls.analytic_account.id,
                    'debit': 100,
                }),
                (0, 0, {
                    'account_id': cls.asset.id,
                    'credit': 100,
                }),
            ],
        })

        cls.debit = cls.move_1.line_ids.filtered(lambda l: l.debit)

    def test_if_expense_account__analytic_line_is_not_revenue(self):
        self.move_1.post()
        assert self.debit.analytic_line_ids
        assert not self.debit.analytic_line_ids.revenue

    def test_if_revenue_account__analytic_line_is_revenue(self):
        self.debit.account_id = self.revenue
        self.move_1.post()
        assert self.debit.analytic_line_ids.revenue
