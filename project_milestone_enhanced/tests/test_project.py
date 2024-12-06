# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProject(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.project = self.env["project.project"].create(
            {"name": "My Project", "allow_milestones": True}
        )

        self.milestone = self.env["project.milestone"].create(
            {"name": "My Milestone", "project_id": self.project.id}
        )

        self.milestone_2 = self.env["project.milestone"].create(
            {"name": "My Milestone 2", "project_id": self.project.id}
        )

        self.task = self.env["project.task"].create(
            {
                "name": "My Task",
                "project_id": self.project.id,
                "milestone_id": self.milestone.id,
            }
        )

        self.task_2 = self.env["project.task"].create(
            {
                "name": "My Task 1",
                "project_id": self.project.id,
                "milestone_id": self.milestone.id,
                "active": False,
            }
        )

        self.task_3 = self.env["project.task"].create(
            {
                "name": "My Task 2",
                "project_id": self.project.id,
                "milestone_id": self.milestone.id,
            }
        )

        self.test_close_stage = self.env["project.task.type"].create(
            {"name": "TestCloseStage", "fold": True}
        )

    def test_copy_project(self):
        project = self.project.copy({})
        tasks = project.with_context(active_test=False).task_ids
        milestone = project.milestone_ids.filtered(
            lambda milestone: "2" not in milestone.name
        )
        assert tasks[0].milestone_id == milestone and tasks[1].milestone_id == milestone

    def test_copy_project_not_milestones(self):
        project = self.project.with_context(milestones_no_copy=True).copy({})
        assert not project.with_context(active_test=False).milestone_ids

    def test_milestone_change_project(self):
        new_project = self.project.copy({})
        self.milestone.project_id = new_project.id
        assert not self.milestone.task_ids

    def test_project_change_allow_milestones(self):
        self.milestone_2.toggle_active()
        self.project.allow_milestones = False
        assert not self.milestone.active
        self.project.allow_milestones = True
        assert self.milestone.active
        assert not self.milestone_2.active

    def test_project_change_active(self):
        self.milestone_2.toggle_active()
        self.project.toggle_active()
        assert not self.milestone.active
        self.project.toggle_active()
        assert self.milestone.active
        assert not self.milestone_2.active

    def test_milestone_progress(self):
        milestone1 = self.milestone

        self.task.stage_id = self.test_close_stage.id
        self.assertEqual(milestone1.progress, 50)

        self.task_3.stage_id = self.test_close_stage.id
        self.assertEqual(milestone1.progress, 100)
