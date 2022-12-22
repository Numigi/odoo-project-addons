# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_task_analytic_lines.tests.common import InvoiceCase


class TestTaskPropagation(InvoiceCase):
    """Run the same tests with a customer invoice.

    The behavior should be the same.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_cost = 40
        cls.product = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'standard_price': cls.product_cost,
            'property_valuation': 'real_time',
        })
        cls.invoice.type = 'out_invoice'
        cls.invoice.invoice_line_ids.product_id = cls.product

    def test_task_propagated_to_cost_move_line(self):
        self._validate_invoice()
        move_line = self.invoice.move_id.line_ids.filtered(
            lambda l: l.debit == self.product_cost)
        assert len(move_line) == 1
        assert move_line.task_id == self.task
