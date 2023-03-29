# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class AccountCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.account_user = cls.env["res.users"].create(
            {
                "name": "Account User",
                "login": "account_user",
                "email": "account_user@test.com",
                "groups_id": [
                    (4, cls.env.ref("account.group_account_invoice").id)],
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

class InvoiceCase(AccountCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Partner A"}
        )

        cls.tax_account = cls.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    cls.env.ref("account.data_account_type_receivable").id,
                )
            ],
            limit=1,
        )

        cls.tax = cls.env["account.tax"].create(
            {
                "name": "10% tax",
                "amount_type": "percent",
                "amount": 0.10,
                #"account_id": cls.tax_account.id,
            }
        )

        cls.invoice = cls.env["account.move"].create(
            {
                "partner_id": cls.partner.id,
                #"project_id": cls.project.id,
                "move_type": "in_invoice",
                #"account_id": cls.payable_account.id,
                "invoice_line_ids": [(0, 0, cls._get_invoice_line_vals())],
            }
        )

    @classmethod
    def _get_invoice_line_vals(cls, **kwargs):
        defaults = {
            "name": "/",
            "quantity": 1,
            #"uom_id": cls.env.ref("uom.product_uom_unit").id,
            "price_unit": 100,
            "analytic_account_id": cls.analytic_account.id,
            "task_id": cls.task.id,
            "account_id": cls.expense_account.id,
            "tax_ids": [(4, cls.tax.id)],
        }
        defaults.update(kwargs)
        return defaults

    def _validate_invoice(self):
        self.invoice.invoice_date = '2023-01-01'
        self.invoice.sudo(self.account_user).action_post()
