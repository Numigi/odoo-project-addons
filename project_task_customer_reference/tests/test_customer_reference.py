# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ..controllers.portal import Portal
from odoo.tests.common import SavepointCase
from odoo.addons.test_http_request.common import mock_odoo_request


class TestCustomerReference(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = cls.env["project.task"].create(
            {
                "name": "test_task",
                "customer_reference": "old",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Participant 1",
                "email": "participant1@example.com",
            }
        )

        cls.user = cls.env["res.users"].create(
            {
                "partner_id": cls.partner.id,
                "email": "participant@example.com",
                "login": "participant",
                "name": "Participant",
            }
        )

    def test_sign_controller(self):
        new_reference = "new"
        self._update_reference(new_reference)
        assert self.task.customer_reference == new_reference

    def _update_reference(self, new_reference):
        env = self.env(user=self.user.id)
        with mock_odoo_request(env, routing_type="http"):
            return Portal().task_update_customer_reference(
                self.task.id,
                reference=new_reference,
            )
