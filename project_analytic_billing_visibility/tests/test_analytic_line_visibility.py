# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytest
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestAnalyticLineVisibility(TransactionCase):

    def setUp(self):
        super().setUp()
        self._setup_users()
        self._setup_analytic_data()

    def _setup_users(self):
        self.manager = self.env["res.users"].create({
            "name": "Test Manager",
            "login": "test_manager",
            "groups_id": [(4, self.env.ref("project.group_project_manager").id)],
        })
        self.standard_user = self.env["res.users"].create({
            "name": "Test User",
            "login": "test_user",
            "groups_id": [(4, self.env.ref("base.group_user").id)],
        })

    def _setup_analytic_data(self):
        self.account = self.env["account.analytic.account"].create({"name": "Test"})
        self.move = self.env["account.move"].sudo().create({"move_type": "entry"})

        self.move_line = self.env["account.move.line"].sudo().create({
            "move_id": self.move.id,
            "name": "Test Move Line",
            "account_id": self.env.ref("account.data_account_type_revenue").id,
        })

        self.analytic_line = self.env["account.analytic.line"].sudo().create({
            "name": "Test Analytic Line",
            "account_id": self.account.id,
            "move_id": self.move_line.id,
        })

    def test_manager_can_read_billing_line(self):
        record = self.analytic_line.with_user(self.manager)
        assert record.read(["name"])

    def test_standard_user_cannot_read_billing_line(self):
        record = self.analytic_line.with_user(self.standard_user)
        with pytest.raises(AccessError):
            record.read(["name"])
