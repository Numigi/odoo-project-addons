# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests import common


class OutsourcingCase(common.TransactionCase):

    def setUp(self):
        super(OutsourcingCase, self).setUp()

        self.project_user = self.env["res.users"].create(
            {
                "name": "Project User",
                "login": "project_user",
                "email": "project_user@test.com",
                "groups_id": [
                    (4, self.env.ref("project.group_project_user").id)
                ],
            }
        )

        self.purchase_user = self.env["res.users"].create(
            {
                "name": "Purchase User",
                "login": "purchase_user",
                "email": "purchase_user@test.com",
                "groups_id": [
                    (4, self.env.ref("purchase.group_purchase_user").id)
                ],
            }
        )

        self.supplier = self.env["res.partner"].create({
            "name": "Supplier A",
            "is_company": True,
            "subcontracting_auto_time_entries": True,
            "employee_id": self.env.ref("hr.employee_admin").id,
        })

        self.supplier_child = self.env["res.partner"].create({
            "name": "Supplier Child A",
            "company_type": 'person',
            "parent_id": self.supplier.id,
        })

        self.project = self.env["project.project"].create({"name": "Job 123"})

        self.stage_new = self.env.ref("project.project_stage_0")
        self.stage_done = self.env.ref("project.project_stage_2")
        self.stage_done.write({
            "create_subcontractors_time_entries": True
        })
        self.stage_test = self.env["project.task.type"].create({
            "name": "Client Test",
            "create_subcontractors_time_entries": True
        })
        self.task = self.env["project.task"].create({
            "name": "Task 450",
            "project_id": self.project.id,
            "stage_id": self.stage_new.id,
        })

        self.product = self.env["product.product"].create({
            "name": "Outsourcing",
            "type": "service",
            "automate_time_entries": True
        })

        self.po_order = self.env["purchase.order"].create(
            {
                "partner_id": self.supplier.id,
                "is_outsourcing": True,
                "project_id": self.project.id,
                "task_id": self.task.id,
                "state": 'purchase',
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": "/",
                            "product_qty": 1,
                            "product_uom": self.env.ref(
                                "uom.product_uom_unit").id,
                            "price_unit": 100,
                            "date_planned": datetime.now(),
                        },
                    )
                ],
            }
        )
        self.po_order_2 = self.env["purchase.order"].create(
            {
                "partner_id": self.supplier.id,
                "is_outsourcing": True,
                "project_id": self.project.id,
                "task_id": self.task.id,
                "state": 'draft',
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "name": "/",
                            "product_qty": 1,
                            "product_uom": self.env.ref(
                                "uom.product_uom_unit").id,
                            "price_unit": 100,
                            "date_planned": datetime.now(),
                        },
                    )
                ],
            }
        )
