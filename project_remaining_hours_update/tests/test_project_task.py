# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.tests import common
from odoo.exceptions import AccessError


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'task.user@example.com',
            'email': 'task.user@example.com',
            'login': 'task.user@example.com',
            'groups_id': [
                (4, cls.env.ref('project.group_project_user').id),
            ]
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Project A',
            'privacy_visibility': 'employees',
        })

        cls.planned_hours = 10
        cls.task = cls.env['project.task'].create({
            'name': 'Task',
            'project_id': cls.project.id,
            'planned_hours': cls.planned_hours,
        })

    def test_after_task_created__remaining_hours_is_planned_hours(self):
        assert self.task.remaining_hours == self.planned_hours

    def test_after_task_created__one_history_line_logged(self):
        assert len(self.task.remaining_hours_ids) == 1
        assert self.task.remaining_hours_ids.remaining_hours == self.planned_hours

    def test_after_planned_hours_updated__remaining_hours_is_updated(self):
        new_planned_hours = 12
        self.task.planned_hours = new_planned_hours
        assert self.task.remaining_hours == new_planned_hours

    def test_after_planned_hours_updated__one_history_line_logged(self):
        new_planned_hours = 12
        self.task.planned_hours = new_planned_hours
        assert len(self.task.remaining_hours_ids) == 2

        last_history_line = self.task.remaining_hours_ids.sorted(key='id')
        assert last_history_line[1].remaining_hours == new_planned_hours

    def test_after_update__remaining_hours_is_new_value(self):
        new_value = 9
        self.task.update_remaining_hours(new_value, self.user, comment='Testing')
        assert self.task.remaining_hours == new_value

    def test_update_remaining_hours_is_indempotent(self):
        new_value = 12
        self.task.update_remaining_hours(new_value, self.user, comment='Testing')
        self.task.update_remaining_hours(new_value, self.user, comment='Testing')
        assert self.task.remaining_hours == new_value

    def test_updating_remaining_hours_using_wizard(self):
        new_value = 20
        wizard = self.env['project.task.remaining.hours.update'].sudo(self.user).create({
            'task_id': self.task.id,
            'new_remaining_hours': new_value,
            'comment': 'Harder to develop than expected',
        })
        wizard.validate()
        assert self.task.remaining_hours == new_value

    def test_if_not_write_access__employee_can_not_update_hours(self):
        self.project.privacy_visibility = 'followers'
        task = self.task.sudo(self.user)
        with pytest.raises(AccessError):
            task.update_remaining_hours(10, self.user, comment='Testing')
