# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_material.tests.common import TaskMaterialCase


class TestPreparationStep(TaskMaterialCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse.consu_steps = 'two_steps'
        cls.initial_qty = 10
        cls.line = cls._create_material_line(initial_qty=cls.initial_qty)
        cls.consumption_move = cls.line.move_ids
        cls.preparation_move = cls.line.move_ids.move_orig_ids

    def test_prepared_and_consumed(self):
        self._force_transfer_move(self.preparation_move, 10)
        self._force_transfer_move(self.consumption_move, 10)
        assert not self.line.prepared_versus_initial
        assert not self.line.consumed_versus_initial
        assert not self.line.consumed_versus_prepared

    def test_prepared_and_not_consumed(self):
        self._force_transfer_move(self.preparation_move, 10)
        self._force_transfer_move(self.consumption_move, 1)
        assert not self.line.prepared_versus_initial
        assert self.line.consumed_versus_initial
        assert self.line.consumed_versus_prepared

    def test_not_prepared_and_not_consumed(self):
        self._force_transfer_move(self.preparation_move, 1)
        self._force_transfer_move(self.consumption_move, 1)
        assert self.line.prepared_versus_initial
        assert self.line.consumed_versus_initial
        assert not self.line.consumed_versus_prepared
