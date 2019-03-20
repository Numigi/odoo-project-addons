# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import ProjectIterationCase


class TestTaskParentProject(ProjectIterationCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = cls.env['project.task'].create({
            'name': 'Task 1',
            'project_id': cls.project_1.id,
        })

    def test_parent_project_without_iteration(self):
        self.assertEqual(self.task.parent_project_ids, self.project_1)

    def test_parent_projects_inside_iteration(self):
        self.task.project_id = self.iteration_1
        self.assertEqual(self.task.parent_project_ids, self.iteration_1 | self.project_1)

    def test_parent_projects_after_iteration_parent_changes(self):
        self.task.project_id = self.iteration_1
        self.iteration_1.parent_id = self.project_2
        self.assertEqual(self.task.parent_project_ids, self.iteration_1 | self.project_2)

    def test_parent_projects_after_iteration_parent_is_removed(self):
        self.task.project_id = self.iteration_1
        self.iteration_1.parent_id = False
        self.assertEqual(self.task.parent_project_ids, self.iteration_1)
