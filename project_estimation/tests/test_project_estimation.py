# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from ddt import ddt, data, unpack
from odoo.tests import common


@ddt
class TestProjectEstimation(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {"name": "Project A", "estimation_mode_active": True}
        )

        cls.date_planned = datetime.now().date()

        cls.task = cls.env["project.task"].create(
            {
                "name": "Task A",
                "project_id": cls.project.id,
                "date_planned": cls.date_planned,
            }
        )

    @data(("True", True), ("False", False))
    @unpack
    def test_default_system_parameter(self, param_value, value):
        self.env["ir.config_parameter"].set_param(
            "project_estimation_mode_active_default", param_value
        )
        new_project = self.project.copy()
        assert new_project.estimation_mode_active == value

    def test_enter_estimation(self):
        self.project.estimation_mode_active = False
        wizard = self._make_enter_wizard()
        wizard.validate()
        assert self.project.estimation_mode_active

    def test_exit_estimation(self):
        wizard = self._make_exit_wizard()
        wizard.validate()
        assert not self.project.estimation_mode_active

    def _make_exit_wizard(self):
        return self.env["project.estimation.exit"].create(
            {"project_id": self.project.id}
        )
