# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestTaskTemplate(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestTaskTemplate, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Dave of the Ash',
        })

        cls.project = cls.env['project.project'].create({
            'user_id': cls.env.user.id,
            'name': 'My Test Project',
            'use_tasks': True,
            'partner_id': cls.partner.id,
            'date_start': fields.Date.today(),
        })

        project_model = cls.env['ir.model'].search([
            ('model', '=', 'project.project')
        ], limit=1)

        cls.template = cls.env['project.task.template'].create({
            'model_id': project_model.id,
            'name': 'My Test Task 1',
            'description': 'This should be in project {object.name}.',
            'use_relative_partner_id': True,
            'use_relative_project_id': True,
            'relative_partner_id': 'object.partner_id',
            'relative_project_id': 'object',
        })

        cls.template_2 = cls.env['project.task.template'].create({
            'model_id': project_model.id,
            'name': 'My Test Task 2',
            'description': 'This should be in project {object.name}.',
            'use_relative_project_id': True,
            'relative_project_id': 'object',
        })

    def test_create_task_from_record(self):
        task = self.template.create_tasks_from_records(self.project)
        self.assertTrue('My Test Project' in task.description)
        self.assertEqual(task.partner_id, self.partner)

    def test_wrong_relative_format(self):
        with self.assertRaises(ValidationError):
            self.template.write({
                'relative_partner_id': "that's not right!",
            })

    def test_wrong_field_type(self):
        with self.assertRaises(ValidationError):
            self.template.write({
                'relative_partner_id': "object.date_start",
            })

    def test_relative_field_no_model_set(self):
        with self.assertRaises(ValidationError):
            self.template.write({
                'model_id': False,
            })

    def test_deadline_relative_to_field(self):
        self.template.write({
            'use_relative_deadline': True,
            'relative_deadline_delta': 3,
            'relative_deadline_units': 'days',
            'relative_deadline_op': 'after',
            'relative_deadline': 'object.date_start',
        })
        task = self.template.create_tasks_from_records(self.project)
        date_start = fields.Date.from_string(self.project.date_start)
        expected = fields.Date.to_string(date_start + timedelta(days=3))
        self.assertEqual(task.date_deadline, expected)

    def test_deadline_relative_to_today(self):
        self.template.write({
            'use_relative_deadline': True,
            'relative_deadline_delta': 2,
            'relative_deadline_units': 'weeks',
            'relative_deadline_op': 'before',
            'relative_deadline': 'today',
        })
        task = self.template.create_tasks_from_records(self.project)
        expected = fields.Date.to_string(date.today() - timedelta(weeks=2))
        self.assertEqual(task.date_deadline, expected)

    def test_create_multiple_tasks_from_record(self):
        templates = self.template | self.template_2
        tasks = templates.create_tasks_from_records(self.project)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].project_id, self.project)
        self.assertEqual(tasks[1].project_id, self.project)
