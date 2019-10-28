# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.tests import common
from odoo.exceptions import ValidationError


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
