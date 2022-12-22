# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_outsourcing.tests.common import OutsourcingCase


class TestOutsourcingPurchaseOrder(OutsourcingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wip_account = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140102',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'reconcile': True,
            'company_id': cls.env.user.company_id.id,
        })
        cls.project_type = cls.env['project.type'].create({
            'name': 'Manufacture',
            'wip_account_id': cls.wip_account.id,
        })
        cls.project.project_type_id = cls.project_type
        cls.order.button_confirm()
        cls.invoice = cls.env['account.invoice'].create({
            'partner_id': cls.supplier.id,
            'type': 'in_invoice',
        })
        cls.expense_account = cls.env['account.account'].create({
            'name': 'Expenses',
            'code': '510101',
            'user_type_id': cls.env.ref('account.data_account_type_expenses').id,
            'company_id': cls.env.user.company_id.id,
        })
        cls.product.property_account_expense_id = cls.expense_account

    def test_wip_account_propagated_to_invoice_line(self):
        values = self.invoice._prepare_invoice_line_from_po_line(self.order.order_line)
        assert values['account_id'] == self.wip_account.id

    def test_if_no_wip_account__default_account_propagated_to_invoice_line(self):
        self.project_type.wip_account_id = False
        values = self.invoice._prepare_invoice_line_from_po_line(self.order.order_line)
        assert values['account_id'] == self.expense_account.id

    def test_on_change_product__wip_account_propagated(self):
        values = self.invoice._prepare_invoice_line_from_po_line(self.order.order_line)
        invoice_line = self.env['account.invoice.line'].create(values)

        with self.env.do_in_onchange():
            invoice_line.account_id = False
            invoice_line.product_id = self.product
            invoice_line._onchange_product_id()
            assert invoice_line.account_id == self.wip_account
