# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.addons.project_iteration.tests.common import ProjectIterationCase

class TestChangeProjectParentWithTimeSheet(ProjectIterationCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = cls.env['project.task'].create({
            'name': 'Task 1',
            'project_id': cls.iteration_1.id,
        })

    def _create_anl(self):
        analytic_account = self.env["account.analytic.account"].create({"name": "ABC"})
        self.env["account.analytic.line"].create({
            "name": "Do something",
            "account_id": analytic_account.id,
            "project_id": self.iteration_1.id
        })

    def test_allow_change_parent_on_project_with_timesheet(self):
        self._create_anl()
        self.iteration_1.parent_id = self.project_2.id

