# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import InvoiceCase


class TestTaskPropagationFromInvoice(InvoiceCase):

    def test_task_propagated_to_expense_move_line(self):
        self._validate_invoice()
        move_line = self.invoice.line_ids.filtered(
            lambda l: l.account_id == self.expense_account)
        assert move_line.task_id == self.task

    def test_task_not_propagated_to_payable_move_line(self):
        self._validate_invoice()
        move_line = self.invoice.line_ids.filtered(
            lambda l: l.account_id == self.payable_account)
        assert len(move_line) == 1
        assert not move_line.task_id
