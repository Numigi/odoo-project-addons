# Copyright 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class ConsumptionRouteCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.user.company_id
        cls.main_warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.user.company_id.id)], limit=1
        )

        cls.new_company = cls.env["res.company"].create({"name": "Test Company 1"})
        cls.new_warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.new_company.id)], limit=1
        )


class TestConsumptionStep(ConsumptionRouteCase):
    def test_default_consumption_location(self):
        assert self.new_warehouse.consu_location_id == self.env.ref(
            "stock_location_production.location_production"
        )

    def test_main_warehouse_has_consumption_route(self):
        assert self.main_warehouse.consu_route_id

    def test_main_warehouse_has_consumption_picking_type(self):
        assert self.main_warehouse.consu_type_id

    def test_main_warehouse_has_consumption_return_picking_type(self):
        assert self.main_warehouse.consu_return_type_id

    def test_warehouse_field_set_on_consumption_route(self):
        assert self.main_warehouse.consu_route_id.warehouse_ids == self.main_warehouse

    def test_warehouse_field_set_on_picking_type(self):
        assert self.main_warehouse.consu_type_id.warehouse_id == self.main_warehouse

    def test_warehouse_field_set_on_return_picking_type(self):
        assert (
            self.main_warehouse.consu_return_type_id.warehouse_id == self.main_warehouse
        )

    def test_main_warehouse_has_consumption_location(self):
        assert self.main_warehouse.consu_location_id

    def test_picking_type_code_is_consumption(self):
        assert self.main_warehouse.consu_type_id.code == "consumption"

    def test_consumption_route_has_one_pull(self):
        assert len(self.main_warehouse.consu_route_id.rule_ids) == 1

    def test_consumption_pull_action_is_move(self):
        pull = self.main_warehouse.consu_route_id.rule_ids
        assert pull.action == "pull"

    def test_consumption_pull_propagate_is_true(self):
        pull = self.main_warehouse.consu_route_id.rule_ids
        assert pull.propagate_cancel is True

    def test_consumption_pull_procure_method_is_make_to_stock(self):
        pull = self.main_warehouse.consu_route_id.rule_ids
        assert pull.procure_method == "make_to_stock"

    def test_consumption_pull_propagate_group_is_set(self):
        pull = self.main_warehouse.consu_route_id.rule_ids
        assert pull.group_propagation_option == "propagate"

    def test_consumption_route_is_warehouse_selectable(self):
        route = self.main_warehouse.consu_route_id
        assert route.warehouse_selectable

    def test_consumption_route_company_is_warehouse_company(self):
        route = self.main_warehouse.consu_route_id
        assert route.company_id == self.company

        route_2 = self.new_warehouse.consu_route_id
        assert route_2.company_id == self.new_company

    def test_consumption_pull_company_is_warehouse_company(self):
        pull = self.main_warehouse.consu_route_id.rule_ids
        assert pull.company_id == self.company

        pull_2 = self.new_warehouse.consu_route_id.rule_ids
        assert pull_2.company_id == self.new_company

    def test_after_warehouse_write__route_is_not_recreated(self):
        route_1 = self.main_warehouse.consu_route_id
        route_2 = self.new_warehouse.consu_route_id
        warehouses = self.main_warehouse | self.new_warehouse
        warehouses.write({"consu_steps": "one_step"})
        warehouses.refresh()
        assert self.main_warehouse.consu_route_id == route_1
        assert self.new_warehouse.consu_route_id == route_2

    def test_after_warehouse_write__pull_are_not_recreated(self):
        # pull_1 = self.main_warehouse.consu_route_id.rule_ids
        # pull_2 = self.new_warehouse.consu_route_id.rule_ids
        warehouses = self.main_warehouse | self.new_warehouse
        # CHECK ME : this will unlink unused rules on v14 and recreated it
        warehouses.write({"consu_steps": "one_step"})
        warehouses.refresh()
        # assert self.main_warehouse.consu_route_id.rule_ids == pull_1
        # assert self.new_warehouse.consu_route_id.rule_ids == pull_2


class TestPreperationStep(ConsumptionRouteCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.prep_location = (
            cls.env["stock.location"]
            .with_company(cls.new_company)
            .create(
                {
                    "name": "Preparation Location",
                    "usage": "internal",
                    "location_id": cls.new_warehouse.view_location_id.id,
                }
            )
        )
        cls.new_warehouse.with_company(cls.new_company).write(
            {
                "consu_steps": "two_steps",
                "consu_prep_location_id": cls.prep_location.id,
            }
        )
        cls.consumption_pull = cls.new_warehouse.consu_route_id.rule_ids[0]
        cls.preparation_pull = cls.new_warehouse.consu_route_id.rule_ids[1]

    def test_preparation_pull_is_from_stock_location(self):
        assert self.preparation_pull.location_src_id == self.new_warehouse.lot_stock_id

    def test_preparation_pull_is_to_preparation_location(self):
        assert self.preparation_pull.location_id == self.prep_location

    def test_preparation_pull_action_is_move(self):
        assert self.preparation_pull.action == "pull"

    def test_preparation_pull_propagate_is_true(self):
        assert self.preparation_pull.propagate_cancel is True

    def test_consumption_pull_procure_method_is_make_to_order(self):
        assert self.consumption_pull.procure_method == "make_to_order"

    def test_preparation_pull_procure_method_is_make_to_stock(self):
        assert self.preparation_pull.procure_method == "make_to_stock"

    def test_preparation_pull_propagate_group_is_set(self):
        assert self.preparation_pull.group_propagation_option == "propagate"

    def test_preparation_pull_company_properly_set(self):
        assert self.preparation_pull.company_id == self.new_company

    def test_preparation_picking_is_internal(self):
        assert self.preparation_pull.picking_type_id.code == "internal"

    def test_preparation_return_picking_is_internal(self):
        assert (
            self.preparation_pull.picking_type_id.return_picking_type_id.code
            == "internal"
        )

    def test_preparation_picking_types_are_bound_together(self):
        preperation_type = self.preparation_pull.picking_type_id
        return_type = preperation_type.return_picking_type_id
        assert return_type.return_picking_type_id == preperation_type

    def test_consumption_pull_is_from_preparation_location(self):
        assert self.consumption_pull.location_src_id == self.prep_location

    def test_consumption_pull_is_to_consumption_location(self):
        assert self.consumption_pull.location_id == self.new_warehouse.consu_location_id

    def test_if_route_set_to_one_step__consu_pull_deactivated(self):
        self.new_warehouse.consu_steps = "one_step"
        assert self.preparation_pull.active is False

    def test_if_route_reset_to_two_steps__consu_pull_reactivated(self):
        # This will unlink rule for two_step
        self.new_warehouse.consu_steps = "one_step"
        # Then recreate a new preparation_pull, consumption_pull still unchanged
        self.new_warehouse.consu_steps = "two_steps"
        assert self.preparation_pull.active is True
        assert (
            self.preparation_pull.id in self.new_warehouse.consu_route_id.rule_ids.ids
        )
