# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import OutsourcingCase


class TestNoStockableProduct(OutsourcingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': 'Customer A',
            'customer': True,
        })
        cls.stockable_product = cls.env['product.product'].create({
            'name': 'Stockable Product',
            'type': 'product',
            'route_ids': [
                (4, cls.env.ref('stock.route_warehouse0_mto').id),
                (4, cls.env.ref('purchase.route_warehouse0_buy').id),
            ],
            'seller_ids': [(0, 0, {
                'name': cls.supplier.id,
            })]
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'order_line': [(0, 0, {
                'product_id': cls.stockable_product.id,
                'name': '/',
                'price_unit': 200,
                'product_uom_qty': 1,
                'product_uom': cls.env.ref('product.product_uom_unit').id,
            })]
        })

    def test_if_is_outsourcing_po__stockable_product_not_allowed(self):
        with pytest.raises(ValidationError):
            self.order.order_line.product_id = self.stockable_product

    def test_on_procurement__outsourcing_po_is_ignored(self):
        self.sale_order.action_confirm()
        new_po = self.env['purchase.order'].search([
            ('partner_id', '=', self.supplier.id),
            ('id', '!=', self.order.id),
        ])
        assert new_po.order_line.product_id == self.stockable_product
