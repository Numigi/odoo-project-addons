# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import ProjectIterationCase


class TestAnalyticLineParentProjects(ProjectIterationCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # due to the dependency on project_task_stage_allow_timesheet of Isidor
        # we need to make sure the project stage allow timesheet to run the tests
        # see TA#1454
        cls.stage_new = cls.env.ref("project.project_stage_data_1")
        cls.stage_new.allow_timesheet = True

        cls.task_1 = cls.env["project.task"].create(
            {"name": "Task 1", "project_id": cls.iteration_1.id}
        )
        cls.task_1.stage_id = cls.stage_new

        cls.task_2 = cls.env["project.task"].create(
            {"name": "Task 2", "project_id": cls.project_2.id}
        )
        cls.task_2.stage_id = cls.stage_new

        cls.line = cls.env["account.analytic.line"].create(
            {"name": "/", "project_id": cls.iteration_1.id, "task_id": cls.task_1.id}
        )

    def test_parent_project_inside_iteration(self):
        assert self.line.parent_project_id == self.project_1

    def test_project_with_no_parent(self):
        self.line.write({"task_id": self.task_2.id, "project_id": self.project_2.id})
        assert not self.line.parent_project_id
