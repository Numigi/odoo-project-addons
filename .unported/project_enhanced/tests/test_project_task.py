# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import SavepointCase


class TestProjectTask(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.project = cls.env["project.project"].create(
            {
                "name": "My Project",
            }
        )

        cls.task = cls.env["project.task"].create(
            {
                "name": "My Task",
                "project_id": cls.project.id,
            }
        )

    def test_project_stays_archived(self):
        self.project.toggle_active()
        self.project.write({"active": True})
        assert not self.project.active

    def test_task_stays_archived(self):
        self.task.toggle_active()
        self.task.write({"active": True})
        assert not self.task.active

    def test_task_stays_archived_project_operation(self):
        self.task.toggle_active()
        self.project.write({"active": True})
        assert not self.task.active
