# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.tests import common
from odoo.exceptions import ValidationError
from ..models.project_task import SHOW_TASK_TEMPLATES


class TestTaskTemplateAddWizard(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stage_1 = cls.env['project.task.type'].create(
            {'name': 'Stage 1', 'sequence': 1})
        cls.stage_2 = cls.env['project.task.type'].create(
            {'name': 'Stage 2', 'sequence': 2})

        cls.project = cls.env['project.project'].create({
            'name': 'Project A',
            'type_ids': [(4, cls.stage_1.id), (4, cls.stage_2.id)],
        })

        cls.template_a = cls.env['project.task'].create(
            {'name': 'Task A', 'is_template': True})
        cls.template_b = cls.env['project.task'].create(
            {'name': 'Task B', 'is_template': True})

        cls.wizard = cls.env['project.task.template.add'].create(
            {'project_id': cls.project.id})

    def _get_new_generated_tasks(self):
        return self.env['project.task'].with_context(**{SHOW_TASK_TEMPLATES: True}).search([
            ('project_id', '=', self.project.id),
        ])

    def test_one_task_created_per_template(self):
        self.wizard.task_template_ids = self.template_a | self.template_b
        self.wizard.validate()
        new_tasks = self._get_new_generated_tasks()
        assert len(new_tasks) == 2

    def test_if_selected_task_not_template__raise_error(self):
        self.template_b.is_template = False
        self.wizard.task_template_ids = self.template_a | self.template_b
        with pytest.raises(ValidationError):
            self.wizard.validate()

    def test_new_added_task_is_template(self):
        self.wizard.task_template_ids = self.template_a
        self.wizard.validate()
        new_task = self._get_new_generated_tasks()
        assert new_task.is_template

    def test_new_added_task_is_a_copy(self):
        self.wizard.task_template_ids = self.template_a
        self.wizard.validate()
        new_task = self._get_new_generated_tasks()
        assert len(new_task) == 1
        assert new_task != self.template_a

    def test_copy_not_in_new_task_name(self):
        self.wizard.task_template_ids = self.template_a
        self.wizard.validate()
        new_task = self._get_new_generated_tasks()
        assert "(copy)" not in new_task.name

    def test_new_task_template_has_no_stage(self):
        self.wizard.task_template_ids = self.template_a
        self.wizard.validate()
        new_task = self._get_new_generated_tasks()
        assert not new_task.stage_id

    def test_template_subtasks_added_to_project(self):
        self.template_b.parent_id = self.template_a
        self.wizard.task_template_ids = self.template_a
        self.wizard.validate()
        new_tasks = self._get_new_generated_tasks()
        assert len(new_tasks) == 2
