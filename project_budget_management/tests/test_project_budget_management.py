# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectBudgetManagement(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_a = cls.env["project.project"].create({"name": "Project A"})
        cls.task_template_a = cls.env["project.task"].create(
            {
                "name": "Task Template A",
                "is_template": True,
                "project_id": cls.project_a.id,
                "min_hours": 1,
                "planned_hours": 2,
                "max_hours": 4,
            }
        )
        cls.task_template_b = cls.env["project.task"].create(
            {
                "name": "Task Template B",
                "is_template": True,
                "project_id": cls.project_a.id,
                "min_hours": 8,
                "planned_hours": 16,
                "max_hours": 32,
            }
        )
        cls.task_c = cls.env["project.task"].create(
            {"name": "Task C", "is_template": False, "project_id": cls.project_a.id}
        )
        cls.task_d = cls.env["project.task"].create(
            {"name": "Task D", "is_template": False, "project_id": cls.project_a.id}
        )
        cls.timesheet_1 = cls.env["account.analytic.line"].create(
            {
                "name": "ts1",
                "project_id": cls.project_a.id,
                "task_id": cls.task_c.id,
                "unit_amount": 1,
            }
        )
        cls.timesheet_2 = cls.env["account.analytic.line"].create(
            {
                "name": "ts2",
                "project_id": cls.project_a.id,
                "task_id": cls.task_c.id,
                "unit_amount": 2,
            }
        )
        cls.timesheet_3 = cls.env["account.analytic.line"].create(
            {
                "name": "ts3",
                "project_id": cls.project_a.id,
                "task_id": cls.task_d.id,
                "unit_amount": 4,
            }
        )
        cls.timesheet_4 = cls.env["account.analytic.line"].create(
            {
                "name": "ts4",
                "project_id": cls.project_a.id,
                "task_id": cls.task_d.id,
                "unit_amount": 8,
            }
        )

    def _get_last_mail_message(self, project_id):
        return self.env["mail.message"].search(
            [("model", "=", "project.project"), ("res_id", "=", project_id)],
            order="id desc",
            limit=1,
        )

    def test_project_remaining_budget(self):
        assert self.project_a.remaining_budget == 3

    def test_project_remaining_budget_for_task_template_add(self):
        new_task = self.env["project.task"].create(
            {
                "name": "Task Template E",
                "is_template": True,
                "project_id": self.project_a.id,
                "min_hours": 16,
                "planned_hours": 32,
                "max_hours": 64,
            }
        )
        assert self.project_a.remaining_budget == 35
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert "added" in mail_message.body
        assert str(new_task.id) in mail_message.body

    def test_project_remaining_budget_for_task_template_unlinked(self):
        self.task_template_b.unlink()
        assert self.project_a.remaining_budget == -13
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert "deleted" in mail_message.body
        assert str(self.task_template_b.id) in mail_message.body

    def test_project_remaining_budget_for_task_template_move_project(self):
        new_project = self.env["project.project"].create({"name": "Project B"})
        self.task_template_b.project_id = new_project.id
        assert self.project_a.remaining_budget == -13
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert "removed" in mail_message.body
        assert str(self.task_template_b.id) in mail_message.body
        mail_message = self._get_last_mail_message(new_project.id)
        assert "added" in mail_message.body
        assert str(self.task_template_b.id) in mail_message.body

    def test_project_remaining_budget_for_task_template_update(self):
        self.task_template_b.write(
            {"min_hours": 64, "planned_hours": 128, "max_hours": 256}
        )
        assert self.project_a.remaining_budget == 115
        mail_message = self._get_last_mail_message(self.project_a.id)
        assert "modified" in mail_message.body
        assert str(self.task_template_b.id) in mail_message.body

    def test_project_remaining_budget_add_timesheet_on_task(self):
        self.env["account.analytic.line"].create(
            {
                "name": "ts1",
                "project_id": self.project_a.id,
                "task_id": self.task_c.id,
                "unit_amount": 16,
            }
        )
        assert self.project_a.remaining_budget == -13

    def test_project_remaining_budget_add_timesheet_on_new_task(self):
        self.env["account.analytic.line"].create(
            {"name": "ts1", "project_id": self.project_a.id, "unit_amount": 16}
        )
        assert self.project_a.remaining_budget == -13

    def test_project_remaining_budget_for_moved_timesheet_in(self):
        project_b = self.env["project.project"].create({"name": "Project B"})
        timesheet_5 = self.env["account.analytic.line"].create(
            {"name": "ts5", "project_id": project_b.id, "unit_amount": 16}
        )
        timesheet_5.write({"project_id": self.project_a.id})
        assert self.project_a.remaining_budget == -13

    def test_project_remaining_budget_for_moved_timesheet_out(self):
        project_b = self.env["project.project"].create({"name": "Project B"})
        task_b = self.env["project.task"].create(
            {"name": "Task B", "project_id": project_b.id}
        )
        self.timesheet_3.write({"project_id": project_b.id, "task_id": task_b.id})
        self.timesheet_4.write({"project_id": project_b.id, "task_id": task_b.id})
        assert self.project_a.remaining_budget == 15

    def test_project_remaining_budget_for_deleted_timesheet(self):
        self.timesheet_4.unlink()
        assert self.project_a.remaining_budget == 11
