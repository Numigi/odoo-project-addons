# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_material.tests.common import TaskMaterialCase


class TestOneStep(TaskMaterialCase):
    def test_progress(self):
        line = self._create_material_line(initial_qty=10)
        consumption_move = line.move_ids
        self._force_transfer_move(consumption_move, 4)
        assert self.task.material_progress == 40  # 4 / 10 * 100

    def test_has_material(self):
        assert not self.task.has_material
        self._create_material_line(initial_qty=1)
        assert self.task.has_material


class TestTwoSteps(TaskMaterialCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse.consu_steps = "two_steps"
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

    def test_progress(self):
        line = self._create_material_line(initial_qty=10)
        preparation_move = line.move_ids.move_orig_ids
        self._force_transfer_move(preparation_move, 4)
        assert self.task.material_progress == 40  # 4 / 10 * 100

    def test_uom_kg(self):
        self._set_product_uom(self.product_a, self.uom_kg)
        line = self._create_material_line(initial_qty=1)
        preparation_move = line.move_ids.move_orig_ids
        self._force_transfer_move(preparation_move, 1)
        assert self.task.material_progress == 0

    def test_units_and_dozens(self):
        product_b = self.product_a.copy()
        self._set_product_uom(product_b, self.uom_dozen)
        line_a = self._create_material_line(initial_qty=1, product=self.product_a)
        line_b = self._create_material_line(initial_qty=2, product=product_b)
        preparation_move = line_a.move_ids.move_orig_ids
        self._force_transfer_move(preparation_move, 1)
        assert self.task.material_progress == 4  # 1 / (1 + 12 * 2) * 100

    def _set_product_uom(self, product, uom):
        product.write({"uom_id": uom.id, "uom_po_id": uom.id})
