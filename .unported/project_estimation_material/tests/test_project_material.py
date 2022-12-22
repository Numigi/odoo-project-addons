# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.addons.project_material.tests.common import TaskMaterialCase


class TestProjectMaterial(TaskMaterialCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project.estimation_mode_active = False

    def test_estimation_mode_active(self):
        line = self._create_material_line()
        assert line.move_ids

    def test_estimation_mode_inactive(self):
        self.project.estimation_mode_active = True
        line = self._create_material_line()
        assert not line.move_ids

    def test_exit_wizard__set_tasks(self):
        wizard = self._make_exit_wizard()
        wizard._set_tasks()
        assert wizard.task_ids == self.task | self.task_2

    def test_exit_wizard__validate(self):
        line = self._create_material_line()
        wizard = self._make_exit_wizard()
        wizard.validate()
        assert line.move_ids

    def _make_exit_wizard(self):
        return self.env["project.estimation.exit"].create(
            {"project_id": self.project.id}
        )
