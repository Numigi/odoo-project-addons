# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create(
            {"name": "My Project", "use_milestones": True}
        )

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
        milestones = project.milestone_ids
        assert task.milestone_id == milestones

    def test_milestone_change_project(self):
        new_project = self.project.copy({})
        self.milestone.project_id = new_project.id
        assert not self.milestone.project_task_ids

    def test_project_change_use_milestones(self):
        self.project.use_milestones = False
        assert not self.milestone.active
        self.project.use_milestones = True
        assert self.milestone.active

    def test_project_change_active(self):
        self.project.toggle_active()
        assert not self.milestone.active
        self.project.toggle_active()
        assert self.milestone.active
