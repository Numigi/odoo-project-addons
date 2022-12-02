# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from datetime import timedelta, datetime


class TestProjectTimesheetTimeControlEmployeePin(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.employee = self.env["hr.employee"].create({
            "name": "Somebody else",
            "pin": 12345,
        })
        self.project = self.env['project.project'].create({
            'name': 'Test project',
            "allow_timesheets": True,
        })
        self.line = self.env['account.analytic.line'].create({
            'date_time': datetime.now() - timedelta(hours=1),
            'task_id': self.task.id,
            'project_id': self.project.id,
            'account_id': self.analytic_account.id,
            'name': 'Test line',
        })

    def test_wizard_with_employee_pin(self):
        """Standalone wizard usage works properly."""
        wizard = self.env["hr.timesheet.switch"].create({
            "name": "Standalone 1",
            "pin": 12345,
            "project_id": self.project.id,
        })
        self.assertEqual(wizard.running_timer_id, self.line)
        self.assertTrue(wizard.running_timer_duration)
        new_act = wizard.with_context(show_created_timer=True).action_switch()
        new_line = self.env[new_act["res_model"]].browse(new_act["res_id"])
        self.assertEqual(new_line.name, "Standalone 1")
        self.assertEqual(new_line.employee_id, self.employee)
