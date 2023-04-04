# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectTimesheetAnalyticUpdate(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.analytic_account_1 = cls.env["account.analytic.account"].create(
            {"id": 1, "name": 1}
        )
        cls.analytic_account_2 = cls.env["account.analytic.account"].create(
            {"id": 2, "name": 2}
        )

        cls.project_b = cls.env["project.project"].create(
            {"name": "projectB",
             "analytic_account_id": cls.analytic_account_1.id}
        )

        cls.timesheet_b = cls.env["account.analytic.line"].create(
            {"name": "TSHT_b", "unit_amount": 0.5,
             "project_id": cls.project_b.id}
        )

        cls.timesheet_c = cls.env["account.analytic.line"].create(
            {"name": "TSHT_c", "unit_amount": 1, "project_id": cls.project_b.id}
        )

    def test_whenProjectChangeAnalyticAccount_thenAnalyticLinesToo(self):
        self.project_b.analytic_account_id = self.analytic_account_2.id

        assert self.project_b.analytic_account_id == self.analytic_account_2
        assert self.timesheet_b.account_id == self.analytic_account_2
        assert self.timesheet_c.account_id == self.analytic_account_2

    def test_if_no_analytic_account__no_warning_raised(self):
        project = self.env["project.project"].new()
        result = project._onchange_account_id()
        assert not result

    def test_if_analytic_account_set__warning_raised(self):
        project = self.env["project.project"].new()
        project.analytic_account_id = self.analytic_account_1
        result = project._onchange_account_id()
        assert "warning" in result
