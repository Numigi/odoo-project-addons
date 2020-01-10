# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_wip_material.tests.common import ProjectWIPMaterialCase
from ..tools import adjust_analytic_line_amount_sign


class TestStockMoveAnalyticLines(ProjectWIPMaterialCase):
    """This test uses the fixture from module project_wip_material.

    The reason is that project_wip_material defines a pattern for
    generating journal entries from stock moves.

    However, the cost report module is generic.
    It does not rely on a specific logic for generating journal entries
    from stock moves.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.initial_qty = 10
        cls.move = cls._create_material_line(initial_qty=cls.initial_qty).move_ids
        cls._force_transfer_move(cls.move)
        cls.analytic_line = cls.move.mapped('account_move_ids.line_ids.analytic_line_ids')

        cls.return_qty = 9
        cls.return_move = cls._return_stock_move(cls.move, cls.return_qty)
        cls.return_analytic_line = cls.return_move.mapped(
            'account_move_ids.line_ids.analytic_line_ids')

    def test_if_outgoing_stock_move__adjusted_quantity_positive(self):
        adjusted_quantity = adjust_analytic_line_amount_sign(
            self.analytic_line, self.analytic_line.unit_amount)
        assert adjusted_quantity == self.initial_qty

    def test_if_incoming_stock_move__adjusted_quantity_negative(self):
        adjusted_quantity = adjust_analytic_line_amount_sign(
            self.return_analytic_line, self.return_analytic_line.unit_amount)
        assert adjusted_quantity == -self.return_qty

    def test_if_outgoing_stock_move__adjusted_unit_cost_positive(self):
        adjusted_unit_cost = adjust_analytic_line_amount_sign(
            self.analytic_line, self.analytic_line.unit_cost)
        assert adjusted_unit_cost == self.product_a_value

    def test_if_incoming_stock_move__adjusted_unit_cost_positive(self):
        adjusted_unit_cost = adjust_analytic_line_amount_sign(
            self.return_analytic_line, self.return_analytic_line.unit_cost)
        assert adjusted_unit_cost == self.product_a_value

    def test_if_analytic_line_not_from_stock_move__quantity_not_adjusted(self):
        unit_amount = 5
        line = self.env['account.analytic.line'].create({
            'account_id': self.project.analytic_account_id.id,
            'name': 'Line 1',
            'unit_amount': unit_amount,
            'amount': -100,
        })
        adjusted_quantity = adjust_analytic_line_amount_sign(line, line.unit_amount)
        assert adjusted_quantity == unit_amount
