# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import ValidationError
from .common import ProjectIterationCase


class TestProjectIteration(ProjectIterationCase):

    def test_project_children_count(self):
        self.assertEqual(self.project_1.children_count, 2)
        self.assertEqual(self.project_2.children_count, 0)

    def test_project_is_parent(self):
        self.assertTrue(self.project_1.is_parent)

    def test_iteration_is_not_parent(self):
        self.assertFalse(self.iteration_1.is_parent)

    def test_project_with_no_children_is_not_parent(self):
        self.assertFalse(self.project_2.is_parent)

    def test_project_with_children_removed_is_not_parent(self):
        self.project_1.write({'child_ids': [(5, 0)]})
        self.assertFalse(self.project_1.is_parent)

    def test_iteration_can_not_have_child_projects(self):
        with self.assertRaises(ValidationError):
            self.iteration_2.parent_id = self.iteration_1

    def test_parent_project_can_not_have_parent(self):
        with self.assertRaises(ValidationError):
            self.project_1.parent_id = self.project_2
