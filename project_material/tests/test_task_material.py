# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest

from datetime import timedelta
from ddt import data, ddt, unpack
from odoo import fields
from odoo.exceptions import ValidationError
from .common import TaskMaterialCase


@ddt
class TestGenerateProcurementsFromTask(TaskMaterialCase):

    def test_if_no_date_planned_on_task__raise_exception(self):
        self.task.date_planned = False
        with pytest.raises(ValidationError):
            self._create_material_line()

    def test_date_planned_on_task_propagated_to_stock_move(self):
        line = self._create_material_line()
        expected_date = fields.Date.from_string(self.task.date_planned)
        move_date = fields.Datetime.from_string(line.move_ids.date_expected).date()
        assert move_date == expected_date

    def test_change_date_planned_on_task__date_propagated_to_stock_move(self):
        new_date = fields.Date.from_string(self.task.date_planned) + timedelta(2)
        line = self._create_material_line()
        self.task.date_planned = new_date

        move_date = fields.Datetime.from_string(line.move_ids.date_expected).date()
        assert move_date == new_date

    def test_product_display_name_propagated_to_stock_move(self):
        line = self._create_material_line()
        assert line.move_ids.name == self.product_a.display_name

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

    @data(
        ('task_readonly', True),
        ('task_invisible', False),
        ('task_required', False),
    )
    @unpack
    def test_stock_picking_task_modifiers(self, modifier_field, value):
        line = self._create_material_line()
        picking = line.move_ids.picking_id
        assert picking[modifier_field] is value

    def test_if_reduce_initial_qty__qty_propagated_to_stock_move(self):
        line = self._create_material_line(initial_qty=10)
        line.initial_qty = 5
        assert line.move_ids.product_uom_qty == 5

    def test_if_delete_material_line__move_is_cancelled(self):
        line = self._create_material_line(initial_qty=10)
        line.initial_qty = 0
        assert line.move_ids.state == 'cancel'

    def test_if_delete_material_line__move_removed_from_stock_picking(self):
        line = self._create_material_line(initial_qty=10)
        line.initial_qty = 0
        assert line.move_ids
        assert not line.move_ids.picking_id

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

    def test_if_move_not_done__material_line_can_be_deleted(self):
        line = self._create_material_line()
        line.unlink()
        assert not line.exists()

    def test_if_material_line_deleted__stock_move_cancelled(self):
        line = self._create_material_line()
        move = line.move_ids
        line.unlink()
        assert move.state == 'cancel'

    def test_if_any_move_done__material_line_can_not_be_deleted(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 1)
        with pytest.raises(ValidationError):
            line.unlink()

    def _get_po_line(self, product):
        return self.env['purchase.order.line'].search([('product_id', '=', product.id)])

    def test_if_product_is_not_mto__purchase_order_not_generated(self):
        self._create_material_line()
        po_line = self._get_po_line(self.product_a)
        assert not po_line

    @data('one_step', 'two_steps')
    def test_if_product_is_mto__purchase_order_generated(self, steps):
        self.warehouse.consu_steps = steps
        self.product_a.route_ids |= self.env.ref('stock.route_warehouse0_mto')
        self._create_material_line()
        po_line = self._get_po_line(self.product_a)
        assert po_line

    def test_after_change_task__initial_stock_move_cancelled(self):
        line = self._create_material_line()
        move = line.move_ids
        line.task_id = self.task_2
        assert move.state == 'cancel'

    def test_after_change_task__new_stock_move_created(self):
        line = self._create_material_line()
        initial_move = line.move_ids
        assert len(initial_move) == 1

        line.task_id = self.task_2

        new_move = line.move_ids
        assert len(new_move) == 1
        assert new_move != initial_move

    def test_after_change_product__initial_stock_move_cancelled(self):
        line = self._create_material_line()
        move = line.move_ids
        line.product_id = self.product_b
        assert move.state == 'cancel'

    def test_after_change_product__new_stock_move_created(self):
        line = self._create_material_line()
        initial_move = line.move_ids
        assert len(initial_move) == 1

        line.product_id = self.product_b

        new_move = line.move_ids
        assert len(new_move) == 1
        assert new_move != initial_move

    def test_if_any_move_done__material_line_can_not_change_task(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 1)
        with pytest.raises(ValidationError):
            line.task_id = self.task_2

    def test_if_any_move_done__material_line_can_not_change_product(self):
        line = self._create_material_line(initial_qty=10)
        self._force_transfer_move(line.move_ids, 1)
        with pytest.raises(ValidationError):
            line.product_id = self.product_b

    def test_for_each_material_line__one_stock_move_generated(self):
        """Test each material line generates an independant stock move.

        By default, Odoo attempts to aggregate stock moves with common
        values (group_id, product_id, etc).
        """
        line_1 = self._create_material_line()
        line_2 = self._create_material_line()
        move_1 = line_1.move_ids
        move_2 = line_2.move_ids
        assert move_1
        assert move_2
        assert move_1 != move_2


class TestPreparationStep(TaskMaterialCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse.consu_steps = 'two_steps'
        cls.initial_qty = 10
        cls.line = cls._create_material_line(initial_qty=cls.initial_qty)
        cls.preparation_move = cls.line.move_ids.move_orig_ids

    def test_qty_reduced_on_preparation(self):
        new_qty = 9
        self.line.initial_qty = new_qty
        assert self.preparation_move.product_qty == new_qty

    def test_if_qty_reduced_to_zero__preparation_cancelled(self):
        self.line.initial_qty = 0
        assert self.preparation_move.state == 'cancel'

    def test_if_qty_reduced_to_zero__preparation_unlinked_from_picking(self):
        self.line.initial_qty = 0
        assert not self.preparation_move.picking_id

    def test_for_each_material_line__one_consumption_move_generated(self):
        line_1 = self._create_material_line()
        line_2 = self._create_material_line()
        consumption_move_1 = line_1.move_ids
        consumption_move_2 = line_2.move_ids
        assert consumption_move_1
        assert consumption_move_2
        assert consumption_move_1 != consumption_move_2

    def test_for_each_material_line__one_preparation_move_generated(self):
        line_1 = self._create_material_line()
        line_2 = self._create_material_line()
        preparation_move_1 = line_1.move_ids.move_orig_ids
        preparation_move_2 = line_2.move_ids.move_orig_ids
        assert preparation_move_1
        assert preparation_move_2
        assert preparation_move_1 != preparation_move_2
