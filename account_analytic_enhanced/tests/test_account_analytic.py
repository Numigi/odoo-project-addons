# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestAccountAnalytic(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Customer Task",
                "email": "customer@task.com",
                "customer": True,
            }
        )

        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "My Analytic Account",
                "partner_id": cls.partner.id,
            }
        )

    def test_account_analytic_stays_active(self):
        self.analytic_account.toggle_active()
        self.analytic_account.write({"active": True})
        assert not self.analytic_account.active
