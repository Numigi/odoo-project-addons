# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestMilestoneResponsible(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {"name": "Test", "email": "testing@testmail.com",
             "login": "testing"}
        )
        cls.project_1 = cls.env["project.project"].create(
            {
                "name": "Project 1",
                "use_milestones": True,
                "user_id": cls.user.id,
            }
        )
        cls.milestone_1 = cls.env["project.milestone"].create(
            {"name": "Milestone 1", "project_id": cls.project_1.id}
        )

    def test_onchange_milestone_project(self):
        self.milestone_1._onchange_project_id()
        assert (
            self.milestone_1.user_id.id
            == self.project_1.user_id.id
        )
