# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase
from odoo.exceptions import ValidationError


class TestProjectMilestoneDependencies(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project = cls.env["project.project"].create({"name": "My Project"})

        cls.milestone_1 = cls.env["project.milestone"].create(
            {"name": "Milestone 1", "project_id": cls.project.id}
        )

        cls.milestone_2 = cls.env["project.milestone"].create({
            "name": "Milestone 2",
            "project_id": cls.project.id,
            "child_ids": [(4, cls.milestone_1.id)]
        })

    def test_project_milestone_dependencies_recursion(self):
        with self.assertRaises(ValidationError):
            self.milestone_1.write({"child_ids": [(4, self.milestone_2.id)]})

