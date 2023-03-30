# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestProjectTaskSubTaskSameProject(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env["project.project"].create({"name": "projectA"})
        cls.project_b = cls.env["project.project"].create({"name": "projectB"})
        cls.task = cls.env["project.task"].create(
            {"name": "Parent Task", "project_id": cls.project_a.id}
        )
        cls.subtask = cls.env["project.task"].create(
            {
                "name": "Child Task",
                "project_id": cls.project_a.id,
                "parent_id": cls.task.id,
            }
        )

    def test_if_no_timesheet__project_can_be_changed(self):
        self.task.project_id = self.project_b

    def test_if_project_is_the_same__constraint_not_raised(self):
        self._make_timesheet_line(self.task)
        self.task.project_id = self.project_a

    def test_if_task_has_timesheet__project_can_not_be_changed(self):
        self._make_timesheet_line(self.task)
        with pytest.raises(ValidationError):
            self.task.project_id = self.project_b

    def test_if_subtask_has_timesheet__project_can_not_be_changed(self):
        self._make_timesheet_line(self.subtask)
        with pytest.raises(ValidationError):
            self.task.project_id = self.project_b

    def _make_timesheet_line(self, task):
        return self.env["account.analytic.line"].create(
            {"task_id": task.id, "project_id": task.project_id.id, "name": "/"}
        )
