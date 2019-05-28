# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TaskPropagationCase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_user = cls.env['res.users'].create({
            'name': 'Account User',
            'login': 'account_user',
            'email': 'account_user@test.com',
            'groups_id': [(4, cls.env.ref('account.group_account_invoice').id)],
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
        })

        cls.analytic_account = cls.project.analytic_account_id

        cls.task = cls.env['project.task'].create({
            'name': 'Task 1',
            'project_id': cls.project.id,
        })

        cls.task_2 = cls.env['project.task'].create({
            'name': 'Task 2',
            'project_id': cls.project.id,
        })

        cls.expense_account = cls.env['account.account'].search([
            ('user_type_id', '=', cls.env.ref('account.data_account_type_expenses').id),
        ], limit=1)

        cls.payable_account = cls.env['account.account'].search([
            ('user_type_id', '=', cls.env.ref('account.data_account_type_payable').id),
        ], limit=1)


class TestTaskPropagationFromInvoice(TaskPropagationCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env['res.partner'].create({
            'name': 'Supplier A',
            'supplier': True,
        })

        cls.tax_account = cls.env['account.account'].search([
            ('user_type_id', '=', cls.env.ref('account.data_account_type_receivable').id),
        ], limit=1)

        cls.tax = cls.env['account.tax'].create({
            'name': '10% tax',
            'amount_type': 'percent',
            'amount': 0.10,
            'account_id': cls.tax_account.id,
        })

        cls.invoice = cls.env['account.invoice'].create({
            'partner_id': cls.supplier.id,
            'project_id': cls.project.id,
            'type': 'in_invoice',
            'account_id': cls.payable_account.id,
            'invoice_line_ids': [
                (0, 0, cls._get_invoice_line_vals())
            ]
        })

    @classmethod
    def _get_invoice_line_vals(cls, **kwargs):
        defaults = {
            'name': '/',
            'quantity': 1,
            'uom_id': cls.env.ref('product.product_uom_unit').id,
            'price_unit': 100,
            'account_analytic_id': cls.analytic_account.id,
            'task_id': cls.task.id,
            'account_id': cls.expense_account.id,
            'invoice_line_tax_ids': [(4, cls.tax.id)],
        }
        defaults.update(kwargs)
        return defaults

    def _validate_invoice(self):
        self.invoice.sudo(self.account_user).action_invoice_open()

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
        self.invoice.compute_taxes()
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
