# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestConsumptionRoute(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.main_warehouse = cls.env['stock.warehouse'].search([
            ('company_id', '=', cls.env.user.company_id.id),
        ], limit=1)

    def test_main_warehouse_has_consumption_route(self):
        assert self.main_warehouse.consu_route_id

    def test_main_warehouse_has_consumption_picking_type(self):
        assert self.main_warehouse.consu_type_id

    def test_main_warehouse_has_consumption_location(self):
        assert self.main_warehouse.consu_location_id
