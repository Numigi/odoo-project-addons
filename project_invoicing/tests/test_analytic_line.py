# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from .common import TestAnalyticLineBase


class TestAnalyticLine(TestAnalyticLineBase):

    @classmethod
    def setUpClass(cls):
        super(TestAnalyticLine, cls).setUpClass()
        cls.price_list = cls.env['product.pricelist'].create({
            'name': 'Sale Pricelist',
            'item_ids': [
                (0, 0, {
                    'compute_price': 'fixed',
                    'fixed_price': 50,
                    'product_id': cls.product.id,
                    'applied_on': '0_product_variant',
                }),
            ],
        })
        cls.customer.property_product_pricelist = cls.price_list
        cls.purchase_line = cls.create_analytic_line(4, -120)
        cls.sale_line = cls.create_analytic_line(4, 200)

    def test_01_show_on_project_invoicing(self):
        self.assertTrue(self.purchase_line.show_on_project_invoicing)
        self.assertFalse(self.sale_line.show_on_project_invoicing)

    def test_02_compute_partner_invoice_id(self):
        self.assertEqual(self.purchase_line.partner_invoice_id, self.customer)

    def test_03_sale_price(self):
        self.assertEqual(self.purchase_line.sale_price, 50)

    def test_04_onchange_partner_invoice_id(self):
        self.purchase_line._onchange_partner_invoice_id()
        self.assertEqual(self.purchase_line.final_price, 50)
        self.assertEqual(self.purchase_line.final_total, 200)
