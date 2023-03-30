# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo import fields


class AccountCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_user = cls.env["res.users"].create(
            {
                "name": "Account User",
                "login": "account_user",
                "email": "account_user@test.com",
                "groups_id": [(4, cls.env.ref("account.group_account_invoice").id)],
            }
        )

        cls.project = cls.env["project.project"].create({"name": "Job 1"})

        cls.project_2 = cls.env["project.project"].create({"name": "Job 2"})

        cls.analytic_account = cls.project.analytic_account_id

        cls.task = cls.env["project.task"].create(
            {"name": "Task 1", "project_id": cls.project.id}
        )

        cls.task_2 = cls.env["project.task"].create(
            {"name": "Task 2", "project_id": cls.project.id}
        )

        cls.expense_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_expenses").id,
                )
            ],
            limit=1,
        )

        cls.payable_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_payable").id,
                )
            ],
            limit=1,
        )


class AccountMoveCase(AccountCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "purchase")], limit=1
        )
        cls.move = cls.env["account.move"].create(
            {
                "journal_id": cls.journal.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "/",
                            "account_id": cls.expense_account.id,
                            "analytic_account_id": cls.analytic_account.id,
                            "task_id": cls.task.id,
                            "debit": 100,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "/",
                            "account_id": cls.payable_account.id,
                            "credit": 100,
                        },
                    ),
                ],
            }
        )
        cls.debit = cls.move.line_ids.filtered(lambda l: l.debit)
        cls.credit = cls.move.line_ids.filtered(lambda l: l.credit)


class InvoiceCase(AccountCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.supplier = cls.env["res.partner"].create(
            {"name": "Supplier A", "supplier_rank": 1}
        )

        cls.tax = cls.env["account.tax"].create(
            {
                "name": "10% tax",
                "amount_type": "percent",
                "amount": 0.10,
                "type_tax_use": "purchase",
            }
        )

        cls.invoice = cls.env["account.move"].create(
            {
                "partner_id": cls.supplier.id,
                "move_type": "in_invoice",
                "invoice_line_ids": [(0, 0, cls._get_invoice_line_vals())],
                "invoice_date": fields.Date.from_string('2019-01-01'),
            }
        )

    @classmethod
    def _get_invoice_line_vals(cls, **kwargs):
        defaults = {
            "name": "/",
            "quantity": 1,
            "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
            "price_unit": 100,
            "analytic_account_id": cls.analytic_account.id,
            "task_id": cls.task.id,
            "account_id": cls.expense_account.id,
            "tax_ids": [(4, cls.tax.id)],
        }
        defaults.update(kwargs)
        return defaults

    def _validate_invoice(self):
        self.invoice.with_user(self.account_user).action_post()
