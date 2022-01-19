# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "My Project"})

        cls.milestone = cls.env["project.milestone"].create(
            {"name": "My Milestone", "project_id": cls.project.id}
        )

        cls.task = cls.env["project.task"].create(
            {
                "name": "My Task",
                "project_id": cls.project.id,
                "milestone_id": cls.milestone.id,
            }
        )

    def test_copy_project(self):
        project = self.project.copy({})
        task = project.task_ids
        milestone = project.milestone_ids
        assert task.milestone_id == milestone
