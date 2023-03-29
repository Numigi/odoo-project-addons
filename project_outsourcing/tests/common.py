# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests import common


class OutsourcingCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_user = cls.env["res.users"].create(
            {
                "name": "Project User",
                "login": "project_user",
                "email": "project_user@test.com",
                "groups_id": [
                    (4, cls.env.ref("project.group_project_user").id)],
            }
        )

        cls.purchase_user = cls.env["res.users"].create(
            {
                "name": "Purchase User",
                "login": "purchase_user",
                "email": "purchase_user@test.com",
                "groups_id": [
                    (4, cls.env.ref("purchase.group_purchase_user").id)],
            }
        )

        cls.supplier = cls.env["res.partner"].create(
            {"name": "Partner A"}
        )

        cls.project = cls.env["project.project"].create({"name": "Job 123"})

        cls.task = cls.env["project.task"].create(
            {"name": "Task 450", "project_id": cls.project.id}
        )

        cls.product = cls.env["product.product"].create(
            {"name": "Outsourcing", "type": "service"}
        )

        cls.order = cls.env["purchase.order"].create(
            {
                "partner_id": cls.supplier.id,
                "is_outsourcing": True,
                "project_id": cls.project.id,
                "task_id": cls.task.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "name": "/",
                            "product_qty": 1,
                            "product_uom": cls.env.ref(
                                "uom.product_uom_unit").id,
                            "price_unit": 100,
                            "date_planned": datetime.now(),
                        },
                    )
                ],
            }
        )
