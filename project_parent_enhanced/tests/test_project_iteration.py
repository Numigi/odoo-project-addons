# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProjectIteration(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_1 = cls.env["project.project"].create({"name": "Project 1"})
        cls.project_2 = cls.env["project.project"].create({"name": "Project 2"})

        cls.iteration_1 = cls.env["project.project"].create(
            {
                "name": "Iteration 1",
                "parent_id": cls.project_1.id,
            }
        )
        cls.iteration_2 = cls.env["project.project"].create(
            {
                "name": "Iteration 2",
                "parent_id": cls.project_1.id,
            }
        )

    def test_project_child_ids_count(self):
        assert self.project_1.child_ids_count == 2
        assert self.project_2.child_ids_count == 0

    def test_project_is_parent(self):
        assert self.project_1.is_parent

    def test_iteration_is_not_parent(self):
        assert not self.iteration_1.is_parent

    def test_project_with_no_children_is_not_parent(self):
        assert not self.project_2.is_parent

    def test_project_with_children_removed_is_not_parent(self):
        self.project_1.write({"child_ids": [(5, 0)]})
        assert not self.project_1.is_parent

    def test_parent_project_can_not_have_parent(self):
        with pytest.raises(ValidationError):
            self.project_1.parent_id = self.project_2

    def test_iteration_can_not_have_child_projects(self):
        with pytest.raises(ValidationError):
            self.iteration_2.parent_id = self.iteration_1.id
