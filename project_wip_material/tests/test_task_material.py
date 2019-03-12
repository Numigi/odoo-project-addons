# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from datetime import datetime
from odoo.exceptions import ValidationError
from .common import TaskMaterialCase


class TestGenerateProcurementsFromTask(TaskMaterialCase):

    def test_if_no_date_planned_on_task__raise_exception(self):
        self.task.date_planned = False
        with pytest.raises(ValidationError):
            self._create_material_line()

    def test_if_no_warehouse_on_project__raise_exception(self):
        self.project.warehouse_id = False
        with pytest.raises(ValidationError):
            self._create_material_line()

    def test_on_add_material__stock_move_generated(self):
        line = self._create_material_line()
        assert len(line.move_ids) == 1

    def test_product_propagated_to_stock_move(self):
        line = self._create_material_line()
        assert line.move_ids.product_id == self.product_a

    def test_quantity_propagated_to_stock_move(self):
        line = self._create_material_line(initial_qty=10)
        assert line.move_ids.product_uom_qty == 10

    def test_product_uom_propagated_to_stock_move(self):
        uom = self.env.ref('product.product_uom_kgm')
        self.product_a.write({
            'uom_id': uom.id,
            'uom_po_id': uom.id,
        })
        line = self._create_material_line()
        assert line.move_ids.product_uom == uom

    def test_warehouse_route_propagated_to_stock_move(self):
        line = self._create_material_line()
        assert line.move_ids.route_ids == self.route

    def test_stock_move_source_location_is_stock(self):
        line = self._create_material_line()
        assert line.move_ids.location_id == self.warehouse.lot_stock_id

    def test_stock_move_destination_is_consumption_location(self):
        line = self._create_material_line()
        assert line.move_ids.location_dest_id == self.warehouse.consu_location_id

    def test_multiple_products_are_combined_in_same_picking(self):
        line_1 = self._create_material_line(product=self.product_a)
        line_2 = self._create_material_line(product=self.product_b)
        assert line_1.move_ids.picking_id
        assert line_1.move_ids.picking_id == line_2.move_ids.picking_id

    def test_task_propagated_to_stock_picking(self):
        line = self._create_material_line()
        assert line.move_ids.picking_id.task_id == self.task

    def test_project_propagated_to_stock_picking(self):
        line = self._create_material_line()
        assert line.move_ids.picking_id.project_id == self.project

    def test_if_reduce_initial_qty__qty_propagated_to_stock_move(self):
        line = self._create_material_line(initial_qty=10)
        line.initial_qty = 5
        assert line.move_ids.product_uom_qty == 5

    def test_if_delete_material_line__move_is_cancelled(self):
        line = self._create_material_line(initial_qty=10)
        line.initial_qty = 0
        assert line.move_ids.state == 'cancel'

    def test_if_raise_initial_quantity__stock_move_is_increased(self):
        line = self._create_material_line(initial_qty=10)
        line.initial_qty = 20
        assert line.move_ids.product_uom_qty == 20

    def test_if_raise_initial_quantity__if_move_is_done__new_move_created(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids)
        line.initial_qty = 15
        assert len(line.move_ids) == 2

    def test_if_raise_initial_quantity__if_move_is_done__new_move_has_missing_quantity(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids)
        line.initial_qty = 15
        new_move = line.move_ids.filtered(lambda m: m.state != 'done')
        assert new_move.product_uom_qty == 5

    def test_if_move_is_done__can_not_reduce_quantity(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids)
        with pytest.raises(ValidationError):
            line.initial_qty = 9

    def test_if_back_order__initial_qty_can_be_reduced(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 7)
        line.initial_qty = 9
        back_order = line.move_ids.filtered(lambda m: m.state != 'done')
        assert back_order.product_uom_qty == 2  # 9 - 7

    def test_if_back_order__initial_qty_can_be_reduced_to_delivered_quantity(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 7)
        line.initial_qty = 7
        back_order = line.move_ids.filtered(lambda m: m.state != 'done')
        assert back_order.state == 'cancel'

    def test_if_back_order__initial_qty_can_not_be_below_delivered_quantity(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 7)
        with pytest.raises(ValidationError):
            line.initial_qty = 6

    def test_if_back_order__initial_qty_can_be_increased(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 7)
        line.initial_qty = 11
        back_order = line.move_ids.filtered(lambda m: m.state != 'done')
        assert back_order.product_uom_qty == 4  # 11 - 7

    def test_if_move_not_done__no_consumed_quantity(self):
        line = self._create_material_line(initial_qty=10)
        assert not line.consumed_qty

    def test_if_move_done__consumed_quantity_is_done_quantity(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 7)
        assert line.consumed_qty == 7

    def test_returned_moves_substracted_from_consumed_quantity(self):
        line = self._create_material_line(initial_qty=10)
        move = line.move_ids
        self._force_transfer_move(move, 7)
        self._return_stock_move(move, 2)
        assert line.consumed_qty == 5  # 7 - 2
