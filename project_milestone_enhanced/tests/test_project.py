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

        cls.project_template = cls.env["project.project"].create(
            {
                "name": "My Template Project",
            }
        )

        cls.milestone = cls.env["project.milestone"].create(
            {"name": "My Milestone", "project_id": cls.project.id}
        )

        cls.milestone_2 = cls.env["project.milestone"].create(
            {"name": "My Milestone 2", "project_id": cls.project.id}
        )

        cls.task = cls.env["project.task"].create(
            {
                "name": "My Task",
                "project_id": cls.project.id,
                "milestone_id": cls.milestone.id,
            }
        )

        cls.task_2 = cls.env["project.task"].create(
            {
                "name": "My Task 1",
                "project_id": cls.project.id,
                "milestone_id": cls.milestone.id,
                "active": False,
            }
        )

    def test_copy_project(self):
        project = self.project.copy({})
        tasks = project.with_context(active_test=False).task_ids
        milestone = project.milestone_ids.filtered(lambda milestone: not "2" in milestone.name)
        assert tasks[0].milestone_id == milestone and tasks[1].milestone_id == milestone

    def test_copy_project_not_milestones(self):
        project = self.project.with_context(milestones_no_copy=True).copy({})
        assert not project.with_context(active_test=False).milestone_ids

    def test_milestone_change_project(self):
        new_project = self.project.copy({})
        self.milestone.project_id = new_project.id
        assert not self.milestone.project_task_ids

    def test_project_change_use_milestones(self):
        self.milestone_2.toggle_active()
        self.project.use_milestones = False
        assert not self.milestone.active
        self.project.use_milestones = True
        assert self.milestone.active
        assert not self.milestone_2.active

    def test_project_change_active(self):
        self.milestone_2.toggle_active()
        self.project.toggle_active()
        assert not self.milestone.active
        self.project.toggle_active()
        assert self.milestone.active
        assert not self.milestone_2.active

    def test_onchange_project(self):
        self.task._onchange_project()
        assert not self.task.milestone_id
