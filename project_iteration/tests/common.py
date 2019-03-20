# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class ProjectIterationCase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_1 = cls.env['project.project'].create({'name': 'Project 1'})
        cls.project_2 = cls.env['project.project'].create({'name': 'Project 2'})

        cls.iteration_1 = cls.env['project.project'].create({
            'name': 'Iteration 1',
            'parent_id': cls.project_1.id,
        })
        cls.iteration_2 = cls.env['project.project'].create({
            'name': 'Iteration 2',
            'parent_id': cls.project_1.id,
        })
