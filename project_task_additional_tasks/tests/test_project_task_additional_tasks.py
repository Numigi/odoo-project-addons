# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# do a test creating task form and change parent_id to see if is_additional is set
# correctly
from odoo.tests import common, Form


class TestProjectTaskAdditionalTasks(common.TransactionCase):
    def setUp(self):
        super().setUp()

    def test_project_task_is_additional_default(self):
        with Form(self.env['project.task']) as task_form:
            task_form.name = 'Task 1'
        task = task_form.save()
        self.assertFalse(task.is_additional)

        self.env.context = dict(self.env.context, default_parent_id=task.id)

        with Form(self.env['project.task']) as task2_form:
            task2_form.name = 'Subtask for Task 1'
        task2 = task2_form.save()
        self.assertTrue(task2.is_additional)

    def test_project_task_is_additional(self):
        with Form(self.env['project.task']) as task_form:
            task_form.name = 'Task 1'
        task = task_form.save()
        self.assertFalse(task.is_additional)

        with Form(self.env['project.task']) as task2_form:
            task2_form.name = 'Subtask for Task 1'
            task2_form.parent_id = task
        task2 = task2_form.save()
        self.assertTrue(task2.is_additional)
