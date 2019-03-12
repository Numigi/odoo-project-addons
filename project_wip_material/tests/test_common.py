# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import TaskMaterialCase


class TestTaskMaterialFixture(TaskMaterialCase):
    """Test that the TaskMaterialCase works properly."""

    def test_force_transfer_move__move_state_set_to_done(self):
        """Test the _return_stock_move utility method."""
        move = self._create_material_line(initial_qty=1).move_ids
        self._force_transfer_move(move, 1)
        assert move.state == 'done'

    def test_force_transfer_move__expected_moved_quantity(self):
        """Test the _return_stock_move utility method."""
        move = self._create_material_line(initial_qty=10).move_ids
        self._force_transfer_move(move, 7)
        assert move.product_uom_qty == 7

    def test_return_stock_move__picking_code_is_consumption_return(self):
        """Test the _return_stock_move utility method."""
        move = self._create_material_line(initial_qty=1).move_ids
        self._force_transfer_move(move, 1)
        return_move = self._return_stock_move(move, 1)
        assert return_move.picking_code == 'consumption_return'

    def test_return_stock_move__picking_state_is_done(self):
        move = self._create_material_line(initial_qty=1).move_ids
        self._force_transfer_move(move, 1)
        return_move = self._return_stock_move(move, 1)
        assert return_move.state == 'done'

    def test_return_stock_move__expected_quantity_moved(self):
        move = self._create_material_line(initial_qty=10).move_ids
        self._force_transfer_move(move, 10)
        return_move = self._return_stock_move(move, 7)
        assert return_move.product_uom_qty == 7

    def test_return_stock_move__move_has_expected_locations(self):
        move = self._create_material_line(initial_qty=1).move_ids
        self._force_transfer_move(move, 1)
        return_move = self._return_stock_move(move, 1)
        assert return_move.location_id == self.warehouse.consu_location_id
        assert return_move.location_dest_id == self.warehouse.lot_stock_id
