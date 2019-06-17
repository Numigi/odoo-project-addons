# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests import common


class TestWaitingForInvoices(common.SavepointCase):
    """Test the Waiting For Invoices section."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
        })

        cls.analytic_account = cls.project.analytic_account_id

        cls.product = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'service',
        })

        cls.report = cls.env['project.cost.report'].create({})

        cls.supplier = cls.env['res.partner'].create({
            'name': 'My Supplier',
            'supplier': True,
        })

        cls.ordered_quantity = 10
        cls.price_unit = 50

        cls.po = cls.env['purchase.order'].create({
            'partner_id': cls.supplier.id,
            'order_line': [
                (0, 0, {
                    'product_id': cls.product.id,
                    'name': '/',
                    'product_qty': cls.ordered_quantity,
                    'product_uom': cls.env.ref('product.product_uom_unit').id,
                    'price_unit': cls.price_unit,
                    'date_planned': datetime.now(),
                }),
            ]
        })
        cls.po.order_line.account_analytic_id = cls.analytic_account
        cls.po.button_confirm()

    def get_pending_purchase_orders(self):
        return self.report._get_rendering_variables(self.project, {})['pending_purchase_orders']

    def test_if_invoice_not_received__po_in_section(self):
        pending_orders = self.get_pending_purchase_orders()
        assert len(pending_orders) == 1
        assert pending_orders[0].order == self.po

    def _set_invoiced_qty(self, qty):
        self.po.order_line.qty_invoiced = qty

    def test_if_po_draft__po_not_in_section(self):
        self.po.state = 'draft'
        pending_orders = self.get_pending_purchase_orders()
        assert len(pending_orders) == 0

    def test_if_po_done__po_in_section(self):
        self.po.state = 'done'
        pending_orders = self.get_pending_purchase_orders()
        assert len(pending_orders) == 1

    def test_if_po_paid__po_not_in_section(self):
        self._set_invoiced_qty(self.ordered_quantity)
        pending_orders = self.get_pending_purchase_orders()
        assert len(pending_orders) == 0

    def test_if_po_partially_paid__po_in_section(self):
        self._set_invoiced_qty(self.ordered_quantity - 1)
        pending_orders = self.get_pending_purchase_orders()
        assert len(pending_orders) == 1

    def test_if_displayed_amount_is_based_on_quantity_to_invoice(self):
        invoiced_qty = 6
        self._set_invoiced_qty(invoiced_qty)
        pending_orders = self.get_pending_purchase_orders()

        expected_amount = 200  # (ordered_quantity - invoiced_qty) * price_unit
        assert pending_orders[0].total == expected_amount
