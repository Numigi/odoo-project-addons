# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.project_material.tests.common import TaskMaterialCase


class TestTask(TaskMaterialCase):
    def test_copy_task(self):
        self.project.estimation_mode_active = True
        line = self._create_material_line()
        new_task = self.task.copy()
        new_line = new_task.material_line_ids
        assert len(new_line) == 1
        assert new_line != line

    def test_copy_task__estimation_mode_inactive(self):
        self.project.estimation_mode_active = False
        line = self._create_material_line()
        new_task = self.task.copy()
        assert not new_task.material_line_ids

    def test_copy_task__direct_consumption(self):
        self.project.estimation_mode_active = True
        line = self._create_material_line()
        line.is_direct_consumption = True
        new_task = self.task.copy()
        assert not new_task.material_line_ids
