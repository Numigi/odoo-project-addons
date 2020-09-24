# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectIterationSaleInheritance(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_1 = cls.env["project.project"].create({"name": "P1"})
        cls.product_a = cls.env["product.template"].create(
            {
                "name": "A1",
                "type": "service",
                "service_policy": "delivered_timesheet",
                "service_tracking": "project_only",
            }
        )
        cls.partner = cls.env["res.partner"].create({"name": "partner"})

    def test_child_project_get_sales_info_from_parent(self):
        sale_order = self.env["sale.order"].create(
            {
                "name": "SO001",
                "partner_id": self.partner.id,
                "order_line": [(0, 0, {
                    "product_id": self.product_a.product_variant_id.id,
                    "product_uom_qty": 10,
                })]
            }
        )
        sale_order.action_confirm()
        sale_project = sale_order.project_ids[0]
        self.project_1.parent_id = sale_project.id
        self.project_1._onchange_parent_inherit_sale_object()
        self.assertEqual(self.project_1.sale_order_id, sale_project.sale_order_id)
        self.assertEqual(self.project_1.sale_line_id, sale_project.sale_line_id)
