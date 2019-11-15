# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestProjectTaskSubTaskSameProject(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env['project.project'].create({'name': 'projectA'})
        cls.project_b = cls.env['project.project'].create({'name': 'projectB'})
        cls.task_parent = cls.env['project.task'].create({
            'name': 'Task Parent', 'project_id': cls.project_a.id
        })
        cls.subtask_1 = cls.env['project.task'].create({
            'name': 'Task Child 1',
            'project_id': cls.task_parent.project_id.id,
            'parent_id': cls.task_parent.id,
            'min_hours': 0.5,
            'planned_hours': 1.0,
            'max_hours': 2.0
        })
        cls.subtask_2 = cls.env['project.task'].create({
            'name': 'Task Child 2',
            'project_id': cls.task_parent.project_id.id,
            'parent_id': cls.task_parent.id,
            'min_hours': 0.5,
            'planned_hours': 1.0,
            'max_hours': 2.0
        })

    def test_whenParentTaskChangeProject_thenSubTaskInheritNewProject(self):
        """
        Given a parent task is on project A
        And the subtasks are on project A too

        When the parent task is changed to project B

        Then the subtasks are changed to project B too.
        """
        self.task_parent.project_id = self.project_b.id

        assert self.subtask_1.project_id == self.project_b
        assert self.subtask_2.project_id == self.project_b

    def test_onSubTaskAction_noProjectFilterApplied(self):
        res = self.task_parent.action_subtask()
        assert 'search_default_project_id' not in res['context']

    def test_onUpdateSubtask_ifNotSameProject_raiseError(self):
        with pytest.raises(ValidationError):
            self.subtask_1.project_id = self.project_b
