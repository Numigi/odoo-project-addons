# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import exceptions
from odoo.addons.project_timesheet_time_control.tests.test_project_timesheet_time_control import TestProjectTimesheetTimeControl


class TestWizardPermission(TestProjectTimesheetTimeControl):
    def setUp(self):
        super(TestWizardPermission, self).setUp()

    def test_no_user_error_access_right(self):
        # Running line found, stop the timer
        self.assertEqual(self.task.show_time_control, "stop")
        self.task.button_end_work()
        # No more running lines, cannot stop again
        with self.assertRaises(exceptions.UserError):
            self.task.button_end_work()
        # All lines stopped, start new one and test if wizard action possible
        self.task.invalidate_cache()
        self.assertEqual(self.task.show_time_control, "start")
        start_action = self.task.button_start_work()
        wizard = self._create_wizard(start_action, self.task)
        self.assertIsNotNone(wizard.id)
