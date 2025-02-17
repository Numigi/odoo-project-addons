# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProjectTaskSubTaskSameProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env["project.project"].create({"name": "projectA"})
        cls.project_b = cls.env["project.project"].create({"name": "projectB"})
        cls.task_parent = cls.env["project.task"].create(
            {"name": "Task Parent", "project_id": cls.project_a.id}
        )
        cls.subtask_1 = cls.env["project.task"].create(
            {
                "name": "Task Child 1",
                "project_id": cls.task_parent.project_id.id,
                "parent_id": cls.task_parent.id,
                "planned_hours": 1.0,
            }
        )
        cls.subtask_2 = cls.env["project.task"].create(
            {
                "name": "Task Child 2",
                "project_id": cls.task_parent.project_id.id,
                "parent_id": cls.task_parent.id,
                "planned_hours": 1.0,
            }
        )
        cls.subtask_3 = cls.env["project.task"].create(
            {
                "name": "Task Child 2",
                "project_id": cls.task_parent.project_id.id,
                "parent_id": cls.subtask_2.id,
                "planned_hours": 1.0,
            }
        )

    def test_whenParentTaskChangeProject_thenSubTaskInheritNewProject(self):
        self.task_parent.project_id = self.project_b.id

        assert self.subtask_1.project_id == self.project_b
        assert self.subtask_1.display_project_id == self.project_b

        assert self.subtask_2.project_id == self.project_b
        assert self.subtask_2.display_project_id == self.project_b

        assert self.subtask_3.project_id == self.project_b
        assert self.subtask_3.display_project_id == self.project_b

    def test_onUpdateSubtask_ifNotSameProject_raiseError(self):
        with pytest.raises(ValidationError):
            self.subtask_1.project_id = self.project_b
