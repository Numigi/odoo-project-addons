# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestAccountMoveNoAnalytic(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.env['account.journal'].create({
            'name': 'WIP',
            'code': 'WIP',
            'update_posted': True,
            'type': 'general',
        })

        cls.analytic_account = cls.env['account.analytic.account'].create({
            'name': 'Job 123',
        })
        cls.account_expense = cls.env['account.account'].create({
            'name': 'Cost of Goods Sold',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
        })
        cls.account_wip = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
        })

        cls.move_1 = cls.env['account.move'].create({
            'journal_id': cls.journal.id,
            'line_ids': [
                (0, 0, {
                    'account_id': cls.account_wip.id,
                    'analytic_account_id': cls.analytic_account.id,
                    'debit': 100,
                }),
                (0, 0, {
                    'account_id': cls.account_expense.id,
                    'analytic_account_id': cls.analytic_account.id,
                    'credit': 100,
                }),
            ],
        })
        cls.line_1_1 = cls.move_1.line_ids.filtered(lambda l: l.account_id == cls.account_wip)
        cls.line_1_2 = cls.move_1.line_ids.filtered(lambda l: l.account_id == cls.account_expense)

        cls.move_2 = cls.move_1.copy()
        cls.line_2_1 = cls.move_2.line_ids.filtered(lambda l: l.account_id == cls.account_wip)
        cls.line_2_2 = cls.move_2.line_ids.filtered(lambda l: l.account_id == cls.account_expense)

        cls.moves = cls.move_1 | cls.move_2

    def test_if_no_analytic_not_checked__analytic_entries_created(self):
        self.moves.post()
        assert len(self.line_1_1.analytic_line_ids) == 1
        assert len(self.line_1_2.analytic_line_ids) == 1
        assert len(self.line_2_1.analytic_line_ids) == 1
        assert len(self.line_2_2.analytic_line_ids) == 1

    def test_if_no_analytic_checked__analytic_entries_not_created(self):
        self.move_1.no_analytic_lines = True
        self.moves.post()
        assert len(self.line_1_1.analytic_line_ids) == 0
        assert len(self.line_1_2.analytic_line_ids) == 0
        assert len(self.line_2_1.analytic_line_ids) == 1
        assert len(self.line_2_2.analytic_line_ids) == 1

    def test_no_analytic_checked__existing_analytic_entries_are_deleted(self):
        self.moves.post()
        self.moves.button_cancel()
        assert len(self.line_1_1.analytic_line_ids) == 1
        assert len(self.line_1_2.analytic_line_ids) == 1
        assert len(self.line_2_1.analytic_line_ids) == 1
        assert len(self.line_2_2.analytic_line_ids) == 1

        self.move_1.no_analytic_lines = True
        self.moves.post()
        assert len(self.line_1_1.analytic_line_ids) == 0
        assert len(self.line_1_2.analytic_line_ids) == 0
        assert len(self.line_2_1.analytic_line_ids) == 1
        assert len(self.line_2_2.analytic_line_ids) == 1
