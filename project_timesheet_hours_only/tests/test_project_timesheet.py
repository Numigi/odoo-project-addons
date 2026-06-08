# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import common


class TestProjectTimesheetHoursOnly(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.task = cls.env["project.task"].create({
            "name": "Test Task",
            "project_id": cls.project.id,
        })

    def test_compute_timesheet_excludes_material(self):
        self.env["account.analytic.line"].create({
            "project_id": self.project.id,
            "name": "Material",
            "unit_amount": 15.0,
        })
        self.assertEqual(self.project.total_timesheet_time, 0)

    def test_compute_timesheet_includes_hours(self):
        self.env["account.analytic.line"].create({
            "project_id": self.project.id,
            "task_id": self.task.id,
            "name": "Development",
            "unit_amount": 10.0,
        })
        self.assertEqual(self.project.total_timesheet_time, 10)
