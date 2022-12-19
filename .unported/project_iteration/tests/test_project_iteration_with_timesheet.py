# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import ProjectIterationCase


class TestProjectIterationWithTimeSheet(ProjectIterationCase):

    def _create_timesheet(self, project):
        analytic_account = self.env["account.analytic.account"].create({"name": "ABC"})
        self.env["account.analytic.line"].create({
            "name": "Do something",
            "account_id": analytic_account.id,
            "project_id": project.id,
        })

    def test_block_setting_parent_on_project_with_timesheet(self):
        self._create_timesheet(self.project_1)
        with pytest.raises(ValidationError):
            self.project_1.parent_id = self.project_2

    def test_allow_setting_project_with_timesheet_as_parent(self):
        self._create_timesheet(self.project_1)
        self.project_2.parent_id = self.project_1

    def test_allow_setting_project_without_timesheet_as_parent(self):
        self.project_2.parent_id = self.project_1
