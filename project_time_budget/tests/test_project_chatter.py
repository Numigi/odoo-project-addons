# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectBudgetManagement(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Project A"})
        cls.other_project = cls.env["project.project"].create(
            {"name": "Project B"})
        cls.task_template = cls.env["project.task"].create(
            {
                "name": "Task Template",
                "is_template": True,
                "project_id": cls.project.id,
                "min_hours": 1,
                "planned_hours": 2,
                "max_hours": 4,
            }
        )
        cls.task = cls.env["project.task"].create(
            {"name": "Normal Task", "is_template": False,
             "project_id": cls.project.id}
        )

    def test_task_template_add(self):
        new_task = self.env["project.task"].create(
            {
                "name": "New Task Template",
                "is_template": True,
                "project_id": self.other_project.id,
            }
        )
        body = self._get_last_message_body(self.other_project)
        assert "added" in body
        assert str(new_task.id) in body

    def test_task_template_unlinked(self):
        self.task_template.unlink()
        body = self._get_last_message_body()
        assert "deleted" in body
        assert str(self.task_template.id) in body

    def test_task_template_archived(self):
        self.task_template.active = False
        body = self._get_last_message_body()
        assert "archived" in body
        assert str(self.task_template.id) in body

    def test_task_template_restored(self):
        self.task_template.active = False
        self.task_template.active = True
        body = self._get_last_message_body()
        assert "restored" in body
        assert str(self.task_template.id) in body

    def test_task_template_move_project(self):
        new_project = self.env["project.project"].create({"name": "Project B"})
        self.task_template.project_id = new_project.id

        body = self._get_last_message_body()
        assert "removed" in body
        assert str(self.task_template.id) in body

        body = self._get_last_message_body(new_project)
        assert "added" in body
        assert str(self.task_template.id) in body

    def test_task_template_update(self):
        self.task_template.min_hours = 0
        body = self._get_last_message_body()
        assert "modified" in body
        assert str(self.task_template.id) in body

    def test_task_added(self):
        self.env["project.task"].create(
            {"name": "New Task", "project_id": self.other_project.id}
        )
        body = self._get_last_message_body(self.other_project)
        assert "added" not in body

    def test_task_unlinked(self):
        self.task.unlink()
        body = self._get_last_message_body()
        assert "deleted" not in body

    def test_task_archived(self):
        self.task.active = False
        body = self._get_last_message_body()
        assert "archived" not in body

    def test_task_restored(self):
        self.task.active = False
        self.task.active = True
        body = self._get_last_message_body()
        assert "restored" not in body

    def test_task_move_project(self):
        self.task.project_id = self.other_project

        body = self._get_last_message_body()
        assert "removed" not in body

        body = self._get_last_message_body(self.other_project)
        assert "added" not in body

    def test_task_update(self):
        self.task.min_hours = 0
        body = self._get_last_message_body()
        assert "modified" not in body

    def _get_last_message_body(self, project=None):
        message = self.env["mail.message"].search(
            [
                ("model", "=", "project.project"),
                ("res_id", "=", (project or self.project).id),
            ],
            order="id desc",
            limit=1,
        )
        return message.body or ""
