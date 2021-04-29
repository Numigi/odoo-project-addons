# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestProjectTask(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "project A"})
        cls.task = cls.env["project.task"].create(
            {"name": "Parent Task", "project_id": cls.project.id}
        )
        cls.subtask = cls.env["project.task"].create(
            {
                "name": "Child Task",
                "project_id": cls.project.id,
                "parent_id": cls.task.id,
            }
        )

    def test_search_without_subtasks(self):
        tasks = (
            self.env["project.task"]
            .with_context(no_display_subtasks=True)
            .search([("project_id", "=", self.project.id)])
        )
        assert tasks == self.task

    def test_search_with_subtasks(self):
        tasks = self.env["project.task"].search([("project_id", "=", self.project.id)])
        assert tasks == self.task | self.subtask
