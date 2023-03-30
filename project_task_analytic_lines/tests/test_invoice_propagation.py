# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import InvoiceCase


class TestTaskPropagationFromInvoice(InvoiceCase):

    def test_task_propagated_to_expense_move_line(self):
        self._validate_invoice()
        move_line = self.invoice.move_id.line_ids.filtered(
            lambda l: l.account_id == self.expense_account)
        assert move_line.task_id == self.task

    def test_task_not_propagated_to_payable_move_line(self):
        self._validate_invoice()
        move_line = self.invoice.move_id.line_ids.filtered(
            lambda l: l.account_id == self.payable_account)
        assert len(move_line) == 1
        assert not move_line.task_id

    def test_task_not_propagated_to_tax_move_line(self):
        self._validate_invoice()
        move_line = self.invoice.move_id.line_ids.filtered(
            lambda l: l.account_id == self.tax_account)
        assert len(move_line) == 1
        assert not move_line.task_id

    def test_if_tax_included_in_analytic_cost__task_propagated_to_tax_move_line(self):
        self.tax.analytic = True
        # self.invoice._recompute_dynamic_lines(recompute_all_taxes=True)
        self._validate_invoice()
        move_line = self.invoice.move_id.line_ids.filtered(
            lambda l: l.account_id == self.tax_account)
        assert move_line.task_id == self.task

    def test_move_lines_are_grouped_per_task(self):
        self.invoice.journal_id.group_invoice_lines = True

        self.invoice.write({
            'invoice_line_ids': [
                (0, 0, self._get_invoice_line_vals(task_id=self.task.id)),
                (0, 0, self._get_invoice_line_vals(task_id=self.task_2.id)),
                (0, 0, self._get_invoice_line_vals(task_id=self.task_2.id)),
                (0, 0, self._get_invoice_line_vals(task_id=self.task_2.id)),
                (0, 0, self._get_invoice_line_vals(task_id=False)),
                (0, 0, self._get_invoice_line_vals(task_id=False)),
            ]
        })

        self._validate_invoice()
        move_lines = self.invoice.move_id.line_ids.filtered(
            lambda l: l.account_id == self.expense_account)
        assert len(move_lines) == 3


class TestTaskPropagationFromCustomerInvoice(TestTaskPropagationFromInvoice):
    """Run the same tests with a customer invoice.

    The behavior should be the same.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice.type = 'out_invoice'
