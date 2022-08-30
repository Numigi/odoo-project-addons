# Copyright 2018-2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestProjectMilestoneDomain(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.project = self.env['project.project'].create(
            {'name': 'Test project'})

        self.milestone = self.env['project.milestone'].create({
            'name': 'Milestone',
            'project_id': self.project.id,
        })
        self.role = self.env['project.role'].create({
            'name': 'Role1',
        })
        self.user = self.env.ref("base.user_demo")
        self.assignment = self.env['project.assignment'].create({
            'project_id': self.project.id,
            'milestone_id': self.milestone.id,
            'role_id': self.role.id,
            'user_id': self.user.id,
        })

    def test_onchange_milestone(self):
        record = self.env['project.assignment'].new()
        record.milestone_id = self.milestone.id
        res_onchange_milestone = record.onchange_milestone()
        self.assertEqual(record.project_id, self.project)
        domain = [('id', '=', record.milestone_id.project_id.id)]
        self.assertEqual(res_onchange_milestone['domain']['project_id'], domain)

    def test_onchange_project_id(self):
        record = self.env['project.assignment'].new()
        record.project_id = self.project.id
        res_onchange_project = record.onchange_project()
        domain = [('project_id', '=', record.project_id.id)]
        self.assertTrue(res_onchange_project['domain']['milestone_id'])
        self.assertEqual(res_onchange_project['domain']['milestone_id'], domain)
