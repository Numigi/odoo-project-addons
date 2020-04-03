# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectInheritance(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.account = cls.env["account.analytic.account"].create({"name": "taccount"})
        cls.account1 = cls.env["account.analytic.account"].create({"name": "taccount"})
        cls.project_parent = cls.env["project.project"].create(
            {"name": "tparent", "analytic_account_id": cls.account.id})
        cls.project_parent1 = cls.env["project.project"].create(
            {"name": "tparent1", "analytic_account_id": cls.account1.id})
        cls.project_child = cls.env["project.project"].create({"name": "tchild"})

    def test_whenAccountAndNewParent_thenAccountIsUpdated(self):
        self.project_child.analytic_account_id = self.account1
        assert self.project_child.analytic_account_id != self.project_parent.analytic_account_id
        self.project_child.parent_id = self.project_parent
        assert self.project_child.analytic_account_id == self.project_parent.analytic_account_id

    def test_whenParentChange_thenAccountIsUpdated(self):
        self.project_child.parent_id = self.project_parent1
        assert self.project_child.analytic_account_id != self.project_parent.analytic_account_id
        self.project_child.parent_id = self.project_parent
        assert self.project_child.analytic_account_id == self.project_parent.analytic_account_id

    def test_whenParentAccountChanges_thenAccountOfChildsUpdate(self):
        self.project_child.parent_id = self.project_parent
        self.project_parent.analytic_account_id = self.account1
        assert self.project_child.analytic_account_id == self.project_parent.analytic_account_id
