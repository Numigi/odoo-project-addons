# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from odoo.tests import common
from ..models.project_task import SHOW_TASK_TEMPLATES


@ddt
class TestTaskTemplateAddWizard(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template_a = cls.env['project.task'].create({
            'name': 'Template Task A',
            'is_template': True,
        })
        cls.template_b = cls.env['project.task'].create({
            'name': 'Template Task B',
            'is_template': True,
        })

        cls.task_a = cls.env['project.task'].create({
            'name': 'Task A',
            'is_template': False,
        })
        cls.task_b = cls.env['project.task'].create({
            'name': 'Task B',
            'is_template': False,
        })

    def test_templates_hidden_by_default_from_search(self):
        results = self.env['project.task'].search([('name', 'ilike', 'Task A')])
        assert self.task_a in results
        assert self.template_a not in results

    def test_if_is_template_in_context__templates_not_hidden_from_search(self):
        results = self.env['project.task'].search([
            ('is_template', '=', True),
            ('name', 'ilike', 'Task A'),
        ])
        assert self.task_a not in results
        assert self.template_a in results

    @data(True, False)
    def test_onchange_parent_task__is_template_propagated_to_child(self, new_value):
        self.task_a.is_template = new_value
        self.task_b.is_template = not new_value

        with self.env.do_in_onchange():
            self.task_b.parent_id = self.task_a
            self.task_b._onchange_parent_set_is_template()

        assert self.task_b.is_template == new_value

    @data(True, False)
    def test_on_is_template_write__is_template_propagated_to_child(self, new_value):
        self.task_a.is_template = not new_value
        self.task_b.is_template = not new_value
        self.task_b.parent_id = self.task_a
        self.task_a.is_template = new_value
        assert self.task_b.is_template == new_value

    @data(True, False)
    def test_on_parent_task_write__is_template_propagated_to_child(self, new_value):
        self.task_a.is_template = new_value
        self.task_b.is_template = not new_value
        self.task_b.parent_id = self.task_a
        assert self.task_b.is_template == new_value

    @data(True, False)
    def test_on_subtask_created__is_template_propagated_to_child(self, new_value):
        self.task_a.is_template = new_value
        subtask = self.task_b.copy({'parent_id': self.task_a.id})
        assert subtask.is_template == new_value

    def test_on_subtask_smart_button__display_templates_by_default(self):
        res = self.task_a.action_subtask()
        assert res['context'][SHOW_TASK_TEMPLATES]
