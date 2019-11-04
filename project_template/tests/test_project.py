# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestConvertTemplatesToTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stage_1 = cls.env['project.task.type'].create({'name': 'Stage 1', 'sequence': 1})
        cls.stage_2 = cls.env['project.task.type'].create({'name': 'Stage 2', 'sequence': 2})

        cls.project = cls.env['project.project'].create({
            'name': 'Project A',
            'type_ids': [(4, cls.stage_1.id), (4, cls.stage_2.id)],
        })

        cls.template_a = cls.env['project.task'].create({
            'name': 'Template Task A1',
            'is_template': True,
            'stage_id': False,
        })
        cls.template_b = cls.env['project.task'].create({
            'name': 'Template Task A2',
            'is_template': True,
            'stage_id': False,
        })

    def _get_effective_tasks(self):
        return self.project.task_ids.filtered(lambda t: not t.is_template)

    def test_one_task_created_per_template(self):
        self.template_a.project_id = self.project
        self.template_b.project_id = self.project
        self.project.convert_templates_to_tasks()
        effective_tasks = self._get_effective_tasks()
        assert len(effective_tasks) == 2

    def test_new_subtask_copied_under_new_task(self):
        self.template_a.project_id = self.project
        self.template_b.project_id = self.project
        self.template_b.parent_id = self.template_a
        self.project.convert_templates_to_tasks()
        self._get_effective_tasks()
        task_a = self.template_a.effective_task_ids
        task_b = self.template_b.effective_task_ids
        assert task_b.parent_id == task_a

    def test_new_task_has_first_project_stage(self):
        self.template_a.project_id = self.project
        self.project.convert_templates_to_tasks()
        task_a = self.template_a.effective_task_ids
        assert task_a.stage_id == self.stage_1

    def test_if_same_template_not_converted_twice(self):
        self.template_a.project_id = self.project
        self.project.convert_templates_to_tasks()
        self.project.convert_templates_to_tasks()
        effective_tasks = self._get_effective_tasks()
        assert len(effective_tasks) == 1

    def test_if_child_template_added_afterward__new_subtask_added(self):
        self.template_a.project_id = self.project
        self.project.convert_templates_to_tasks()

        self.template_b.project_id = self.project
        self.template_b.parent_id = self.template_a
        self.project.convert_templates_to_tasks()

        task_a = self.template_a.effective_task_ids
        task_b = self.template_b.effective_task_ids
        assert task_b.parent_id == task_a

    def test_task_template_count(self):
        self.template_a.project_id = self.project
        self.template_b.project_id = self.project
        assert self.project.task_count == 0
        assert self.project.task_template_count == 2

    def test_task_count(self):
        self.template_a.project_id = self.project
        self.template_b.project_id = self.project
        self.template_a.is_template = False
        self.template_b.is_template = False
        assert self.project.task_count == 2
        assert self.project.task_template_count == 0
