# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestProjectMilestoneDependencies(TransactionCase):
    def setUp(self):
        super().setUp()

        self.project = self.env["project.project"].create({"name": "My Project"})

        self.milestone_1 = self.env["project.milestone"].create(
            {"name": "Milestone 1", "project_id": self.project.id}
        )

        self.milestone_2 = self.env["project.milestone"].create(
            {
                "name": "Milestone 2",
                "project_id": self.project.id,
                "child_ids": [(4, self.milestone_1.id)],
            }
        )

    def test_project_milestone_dependencies_recursion(self):
        with self.assertRaises(ValidationError):
            self.milestone_1.write({"child_ids": [(4, self.milestone_2.id)]})

    def test_duplicate_project_milestone_childs(self):
        project_copy = self.project.copy()
        self.assertEqual(len(project_copy.milestone_ids.ids), 2)
        for milestone in project_copy.milestone_ids:
            self.assertFalse(milestone.child_ids)
