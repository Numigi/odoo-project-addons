# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestTaskTemplateAddWizard(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
        })
        cls.template_a = cls.env['project.task'].create({
            'name': 'Template Task A',
            'is_template': True,
            'project_id': cls.project.id,
        })
        cls.template_b = cls.env['project.task'].create({
            'name': 'Template Task B',
            'is_template': True,
            'project_id': cls.project.id,
        })

        cls.task_a = cls.env['project.task'].create({
            'name': 'Task A',
            'is_template': False,
            'project_id': cls.project.id,
        })
        cls.task_b = cls.env['project.task'].create({
            'name': 'Task B',
            'is_template': False,
            'project_id': cls.project.id,
        })

    def _create_timesheet(self, task):
        return self.env['account.analytic.line'].create({
            'project_id': task.project_id.id,
            'task_id': task.id,
            'amount': 1,
            "name": "/",
        })

    def test_can_not_create_timesheet_with_template_task(self):
        with pytest.raises(ValidationError):
            self._create_timesheet(self.template_a)

    def test_timesheet_can_not_be_moved_to_template_task(self):
        line = self._create_timesheet(self.task_a)
        with pytest.raises(ValidationError):
            line.task_id = self.template_a

    def test_task_with_timesheets_can_not_be_set_as_template(self):
        self._create_timesheet(self.task_a)
        with pytest.raises(ValidationError):
            self.task_a.is_template = True

    def test_task_with_subtask_timesheets_can_not_be_set_as_template(self):
        self.task_b.parent_id = self.task_a
        self._create_timesheet(self.task_b)
        with pytest.raises(ValidationError):
            self.task_a.is_template = True
