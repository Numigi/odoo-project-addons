# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from .common import ProjectIterationCase


class TestProjectIteration(ProjectIterationCase):

    def test_project_children_count(self):
        assert self.project_1.children_count == 2
        assert self.project_2.children_count == 0

    def test_project_is_parent(self):
        assert self.project_1.is_parent

    def test_iteration_is_not_parent(self):
        assert not self.iteration_1.is_parent

    def test_project_with_no_children_is_not_parent(self):
        assert not self.project_2.is_parent

    def test_project_with_children_removed_is_not_parent(self):
        self.project_1.write({'child_ids': [(5, 0)]})
        assert not self.project_1.is_parent

    def test_iteration_can_not_have_child_projects(self):
        with pytest.raises(ValidationError):
            self.iteration_2.parent_id = self.iteration_1

    def test_parent_project_can_not_have_parent(self):
        with pytest.raises(ValidationError):
            self.project_1.parent_id = self.project_2

    def test_block_setting_parent_on_project_with_timesheet(self):
        self.env["account.analytic.line"].create({
            "name": "Timesheet 1",
            "project_id": self.project_1.id,
        })
        with pytest.raises(ValidationError):
            self.project_1.parent_id = self.project_2

    def test_allow_setting_project_with_timesheet_as_parent(self):
        self.env["account.analytic.line"].create({
            "name": "Timesheet 2",
        })
        self.project_2.parent_id = self.project_1

    def test_allow_setting_project_without_timesheet_as_parent(self):
        self.project_2.parent_id = self.project_1
