# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestConsumptionRoute(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.user.company_id
        cls.main_warehouse = cls.env['stock.warehouse'].search([
            ('company_id', '=', cls.env.user.company_id.id),
        ], limit=1)

        cls.new_company = cls.env['res.company'].create({
            'name': 'Test Company',
        })
        cls.new_warehouse = cls.env['stock.warehouse'].search([
            ('company_id', '=', cls.new_company.id),
        ], limit=1)

    def test_default_consumption_location(self):
        assert self.new_warehouse.consu_location_id == self.env.ref('stock.location_production')

    def test_main_warehouse_has_consumption_route(self):
        assert self.main_warehouse.consu_route_id

    def test_main_warehouse_has_consumption_picking_type(self):
        assert self.main_warehouse.consu_type_id

    def test_main_warehouse_has_consumption_location(self):
        assert self.main_warehouse.consu_location_id

    def test_picking_type_code_is_consumption(self):
        assert self.main_warehouse.consu_type_id.code == 'consumption'

    def test_consumption_route_has_one_pull(self):
        assert len(self.main_warehouse.consu_route_id.pull_ids) == 1

    def test_consumption_pull_action_is_move(self):
        pull = self.main_warehouse.consu_route_id.pull_ids
        assert pull.action == 'move'

    def test_consumption_route_is_warehouse_selectable(self):
        route = self.main_warehouse.consu_route_id
        assert route.warehouse_selectable

    def test_consumption_route_company_is_warehouse_company(self):
        route = self.main_warehouse.consu_route_id
        assert route.company_id == self.company

        route_2 = self.new_warehouse.consu_route_id
        assert route_2.company_id == self.new_company

    def test_consumption_pull_company_is_warehouse_company(self):
        pull = self.main_warehouse.consu_route_id.pull_ids
        assert pull.company_id == self.company

        pull_2 = self.new_warehouse.consu_route_id.pull_ids
        assert pull_2.company_id == self.new_company

    def test_after_warehouse_write__route_is_not_recreated(self):
        route_1 = self.main_warehouse.consu_route_id
        route_2 = self.new_warehouse.consu_route_id
        warehouses = (self.main_warehouse | self.new_warehouse)
        warehouses.write({'consu_steps': 'one_step'})
        warehouses.refresh()
        assert self.main_warehouse.consu_route_id == route_1
        assert self.new_warehouse.consu_route_id == route_2

    def test_after_warehouse_write__warehouse_has_one_pull(self):
        warehouses = (self.main_warehouse | self.new_warehouse)
        warehouses.write({'consu_steps': 'one_step'})
        warehouses.refresh()
        assert len(self.main_warehouse.consu_route_id.pull_ids) == 1
        assert len(self.new_warehouse.consu_route_id.pull_ids) == 1
