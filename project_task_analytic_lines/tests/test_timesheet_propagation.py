# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import AccountCase


class TestTaskPropagationOnTimesheets(AccountCase):

    def test_on_create__origin_task_filled(self):
        line = self.env['account.analytic.line'].create({
            'name': '/',
            'project_id': self.project.id,
            'task_id': self.task.id,
            'user_id': self.account_user.id,
        })
        assert line.origin_task_id == self.task

    def test_on_write__origin_task_propagated(self):
        line = self.env['account.analytic.line'].create({
            'name': '/',
            'project_id': self.project.id,
            'task_id': self.task.id,
            'user_id': self.account_user.id,
        })
        line.task_id = self.task_2
        assert line.origin_task_id == self.task_2

    def test_on_write_origin_task__task_propagated(self):
        line = self.env['account.analytic.line'].create({
            'name': '/',
            'project_id': self.project.id,
            'task_id': self.task.id,
            'user_id': self.account_user.id,
        })
        line.origin_task_id = self.task_2
        assert line.task_id == self.task_2
