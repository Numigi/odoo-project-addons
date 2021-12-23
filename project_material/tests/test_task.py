# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import TaskMaterialCase


class TestTask(TaskMaterialCase):
    def test_copy_task(self):
        line = self._create_material_line()
        new_task = self.task.copy()
        new_line = new_task.material_line_ids
        assert len(new_line) == 1
        assert new_line != line
        assert new_task.procurement_disabled is True
        assert not new_line.move_ids

    def test_procurement_disabled_unchecked(self):
        self.task.procurement_disabled = True
        line = self._create_material_line()
        assert not line.move_ids
        self.task.procurement_disabled = False
        assert line.move_ids

    def test_procurement_disabled_checked(self):
        line = self._create_material_line()
        assert line.move_ids
        self.task.procurement_disabled = True
        assert not line.move_ids
