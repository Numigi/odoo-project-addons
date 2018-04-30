# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectTaskWithIdInDisplayName(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_a = cls.env['project.task'].create({'name': 'Task A'})
        cls.task_b = cls.env['project.task'].create({'name': 'Task B'})

    def _search_tasks_by_name(self, name):
        """Search tasks given a string to search for.

        :param name: the name of the task to search for
        :return: a recordset of project.task
        """
        ids = [t[0] for t in self.env['project.task'].name_search(name)]
        return self.env['project.task'].browse(ids)

    def test_task_search_by_name(self):
        tasks = self._search_tasks_by_name('Task A')
        self.assertIn(self.task_a, tasks)
        self.assertNotIn(self.task_b, tasks)

    def test_task_search_by_id(self):
        tasks = self._search_tasks_by_name(str(self.task_a.id))
        self.assertIn(self.task_a, tasks)
        self.assertNotIn(self.task_b, tasks)

    def test_display_name(self):
        expected_name = '[{id}] {name}'.format(id=self.task_a.id, name=self.task_a.name)
        self.assertEqual(self.task_a.display_name, expected_name)

    def test_compute_id_string(self):
        self.assertEqual(self.task_a.id, str(self.task_a.id))
