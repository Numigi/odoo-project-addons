# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProject(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProject, cls).setUpClass()

        cls.project = cls.env['project.project'].create({
            'name': 'My Project',
        })

        cls.task_1 = cls.env['project.task'].create({
            'name': 'My Task 1',
            'project_id': cls.project.id,
        })

        cls.task_2 = cls.env['project.task'].create({
            'name': 'My Task 2',
            'project_id': cls.project.id,
        })

        cls.analytic_account = cls.project.analytic_account_id

    def test_01_init(self):
        self.assertTrue(self.project.active)
        self.assertTrue(self.analytic_account.active)
        self.assertTrue(self.task_1.active)
        self.assertTrue(self.task_2.active)

    def test_02_archive_project(self):
        self.project.write({'active': False})

        self.assertFalse(self.project.active)
        self.assertFalse(self.analytic_account.active)
        self.assertFalse(self.task_1.active)
        self.assertFalse(self.task_2.active)

    def test_03_unarchive_project(self):
        self.project.write({'active': False})
        self.project.write({'active': True})

        self.assertTrue(self.project.active)
        self.assertTrue(self.analytic_account.active)
        self.assertFalse(self.task_1.active)
        self.assertFalse(self.task_2.active)
