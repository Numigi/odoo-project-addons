# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestAnalyticLineFields(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
        })

        cls.analytic_account = cls.project.analytic_account_id

        cls.line = cls.env['account.analytic.line'].create({
            'account_id': cls.analytic_account.id,
            'name': 'Line 1',
            'unit_amount': 5,
            'amount': -100,
        })

    def test_if_unit_amount_not_null__unit_cost_is_computed(self):
        assert self.line.unit_cost == 20  # -(-100 / 5)

    def test_if_unit_amount_is_null__unit_cost_is_zero(self):
        self.line.unit_amount = 0
        assert self.line.unit_cost == 0
