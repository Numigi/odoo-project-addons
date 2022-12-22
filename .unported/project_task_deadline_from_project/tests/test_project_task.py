# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date
from odoo.tests import common


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.deadline = date(2018, 6, 1)
        cls.project_with_no_deadline = cls.env['project.project'].create({
            'name': 'Project With No Deadline',
            'date': False,
        })
        cls.project_with_deadline = cls.env['project.project'].create({
            'name': 'Project With Deadline',
            'date': cls.deadline,
        })
        cls.task = cls.env['project.task'].create({'name': 'Task 1'})

    def test_when_creating_task_with_project_then_deadline_is_propagated(self):
        task = self.env['project.task'].create({
            'name': 'Task 2',
            'project_id': self.project_with_deadline.id,
        })
        self.assertEqual(task.date_deadline, self.deadline)

    def test_when_creating_task_with_default_project_then_deadline_is_propagated(self):
        task = self.env['project.task'].with_context(
            default_project_id=self.project_with_deadline.id).create({'name': 'Task 2'})
        self.assertEqual(task.date_deadline, self.deadline)

    def test_when_creating_task_if_project_has_no_deadline_then_deadline_is_empty(self):
        task = self.env['project.task'].create({
            'name': 'Task 2',
            'project_id': self.project_with_no_deadline.id,
        })
        self.assertFalse(task.date_deadline)

    def test_when_changing_project_then_deadline_is_propagated(self):
        self.task.project_id = self.project_with_deadline
        self.assertEqual(self.task.date_deadline, self.deadline)

    def test_when_changing_project_if_project_has_no_deadline_then_deadline_is_empty(self):
        self.task.project_id = self.project_with_no_deadline
        self.assertFalse(self.task.date_deadline)

    def test_onchange_project_then_deadline_is_propagated_to_task(self):
        with self.env.do_in_onchange():
            self.task.project_id = self.project_with_deadline
            self.task._onchange_project_propagate_deadline()

        self.assertEqual(self.task.date_deadline, self.deadline)
