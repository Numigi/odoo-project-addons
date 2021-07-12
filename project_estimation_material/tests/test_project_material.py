# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests import common
from odoo.addons.project_material.tests.common import TaskMaterialCase


class TestProjectMaterial(TaskMaterialCase):
    def test_estimation_mode_active(self):
        line = self._create_material_line()
        assert line.move_ids

    def test_estimation_mode_inactive(self):
        self.project.estimation_mode_active = True
        line = self._create_material_line()
        assert not line.move_ids

    def test_exit_estimation__set_tasks_with_material(self):
        self._create_material_line()
        wizard = self._make_exit_wizard()
        wizard._set_tasks_with_material()
        assert wizard.task_with_material_ids == self.task

    def test_exit_estimation__no_task_no_material(self):
        wizard = self._make_exit_wizard()
        wizard._set_tasks_with_material()
        assert not wizard.task_with_material_ids

    def test_exit_estimation__task_date_planned(self):
        wizard = self._make_exit_wizard()
        wizard.task_with_material_ids = self.task
        wizard.validate()

    def test_exit_estimation__task_with_no_date_planned(self):
        self.task.date_planned = None
        wizard = self._make_exit_wizard()
        wizard.task_with_material_ids = self.task
        with pytest.raises(ValidationError):
            wizard.validate()

    def test_exit_estimation__procurement_executed(self):
        self.project.estimation_mode_active = True
        line = self._create_material_line()
        wizard = self._make_exit_wizard()
        wizard.task_with_material_ids = self.task
        wizard.validate()
        assert line.move_ids

    def _make_exit_wizard(self):
        return self.env["project.estimation.exit"].create(
            {"project_id": self.project.id}
        )
