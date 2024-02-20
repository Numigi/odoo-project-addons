# © 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from odoo.addons.project_material.tests.common import TaskMaterialCase
from odoo.exceptions import AccessError


@ddt
class TestDirectConsumption(TaskMaterialCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.direct_picking_type = cls.env['stock.picking.type'].create({
            'name': 'Direct Consumption',
            'warehouse_id': cls.warehouse.id,
            'company_id': cls.company.id,
            'code': 'consumption',
            'is_direct_consumption': True,
            'sequence_id': cls.env['ir.sequence'].sudo().create({
                'name': 'Direct Consumption',
            }).id,
            'sequence_code': 'DCO',
        })

        cls.picking = cls.env['stock.picking'].create({
            'picking_type_id': cls.direct_picking_type.id,
            'location_id': cls.warehouse.lot_stock_id.id,
            'location_dest_id': cls.env.ref('stock.location_production').id,
            'task_id': cls.task.id,
        })
        cls.quantity = 10
        cls.move = cls.env['stock.move'].create({
            'name': '/',
            'picking_id': cls.picking.id,
            'product_id': cls.product_a.id,
            'product_uom': cls.product_a.uom_id.id,
            'location_id': cls.warehouse.lot_stock_id.id,
            'location_dest_id': cls.env.ref('stock.location_production').id,
            'product_uom_qty': cls.quantity,
        })

    def test_stock_move_is_direct_consumption(self):
        assert self.move.is_direct_consumption

    def test_after_transfer__task_propagated_to_stock_move(self):
        self._force_transfer_move(self.move)
        assert self.move.task_id == self.task

    def test_after_transfer__task_propagated_to__procurement_group(self):
        self._force_transfer_move(self.move)
        assert self.picking.group_id.task_id == self.task

    def test_after_transfer__direct_material_line_created(self):
        self._force_transfer_move(self.move)
        line = self.task.direct_material_line_ids
        assert len(line) == 1
        assert line.product_id == self.product_a
        assert line.initial_qty == 0
        assert line.consumed_qty == self.quantity
        assert line.is_direct_consumption

    @data(
        ('task_readonly', False),
        ('task_invisible', False),
        ('task_required', True),
    )
    @unpack
    def test_picking_task_modifiers__before_transfer(self, modifier_field, value):
        assert self.picking[modifier_field] is value

    @data(
        ('task_readonly', True),
        ('task_invisible', False),
        ('task_required', False),
    )
    @unpack
    def test_picking_task_modifiers__after_transfer(self, modifier_field, value):
        self._force_transfer_move(self.move)
        assert self.picking[modifier_field] is value

    def test_user_can_not_edit_direct_material_line(self):
        self._force_transfer_move(self.move)
        direct_material_line = self.task.direct_material_line_ids

        with pytest.raises(AccessError):
            direct_material_line.initial_qty = 0

    def test_user_can_not_delete_direct_material_line(self):
        self._force_transfer_move(self.move)
        direct_material_line = self.task.direct_material_line_ids

        with pytest.raises(AccessError):
            direct_material_line.unlink()
