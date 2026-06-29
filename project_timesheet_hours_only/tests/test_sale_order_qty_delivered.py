# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common


class TestSaleOrderLineQtyDelivered(common.SavepointCase):
    """Check that the delivered quantity of a timesheet-billed service line
    excludes material consumption (task_id == False) in a mixed project."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.uom_hour = cls.env.ref("uom.product_uom_hour")
        cls.partner = cls.env["res.partner"].create({"name": "Test Customer"})

        cls.analytic_account = cls.env["account.analytic.account"].create({
            "name": "Test Mixed Project - AA",
            "company_id": cls.env.company.id,
        })
        cls.project = cls.env["project.project"].create({
            "name": "Test Mixed Project",
            "allow_timesheets": True,
            "analytic_account_id": cls.analytic_account.id,
        })
        cls.task = cls.env["project.task"].create({
            "name": "Test Task",
            "project_id": cls.project.id,
        })

        # Service product billed on timesheets.
        cls.service_product = cls.env["product.product"].create({
            "name": "Timesheet Service",
            "type": "service",
            "service_type": "timesheet",
            "invoice_policy": "order",
            "uom_id": cls.uom_hour.id,
            "uom_po_id": cls.uom_hour.id,
            "list_price": 100.0,
        })

        cls.order = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
            "analytic_account_id": cls.analytic_account.id,
            "order_line": [(0, 0, {
                "product_id": cls.service_product.id,
                "product_uom_qty": 20.0,
                "product_uom": cls.uom_hour.id,
            })],
        })
        cls.order_line = cls.order.order_line
        cls.project.write({"sale_line_id": cls.order_line.id})
        cls.task.write({"sale_line_id": cls.order_line.id})

    def _create_analytic_line(self, unit_amount, task=None):
        return self.env["account.analytic.line"].create({
            "name": "Line",
            "account_id": self.analytic_account.id,
            "project_id": self.project.id,
            "task_id": task.id if task else False,
            "so_line": self.order_line.id,
            "product_uom_id": self.uom_hour.id,
            "unit_amount": unit_amount,
            "amount": -unit_amount * 50,
        })

    def test_qty_delivered_method_is_timesheet(self):
        self.assertEqual(self.order_line.qty_delivered_method, "timesheet")

    def test_domain_excludes_material(self):
        domain = self.order_line._timesheet_compute_delivered_quantity_domain()
        self.assertIn(("task_id", "!=", False), domain)

    def test_qty_delivered_counts_only_labor(self):
        # 10h of labor (linked to a task).
        self._create_analytic_line(10.0, task=self.task)
        # 5h of "material" (no task) on the same sale order line.
        self._create_analytic_line(5.0, task=None)

        self.order_line._compute_qty_delivered()

        # Only the 10h of labor are counted.
        self.assertEqual(self.order_line.qty_delivered, 10.0)
