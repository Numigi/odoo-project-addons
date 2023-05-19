# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta

from odoo import exceptions
from odoo.tests import common


class TestWizardPermission(common.TransactionCase):
    def setUp(self):
        """
        Based on the module project_timesheet_time_control, the inheritance was not used.
        If inheritance used, it crashed on circleci.
        """
        super().setUp()
        admin = self.browse_ref("base.user_admin")
        # Stop any timer running
        self.env["account.analytic.line"].search(
            [
                ("date_time", "!=", False),
                ("user_id", "=", admin.id),
                ("project_id.allow_timesheets", "=", True),
                ("unit_amount", "=", 0),
            ]
        ).button_end_work()
        admin.groups_id |= self.browse_ref(
            "hr_timesheet.group_hr_timesheet_user")
        self.uid = admin.id
        self.project = self.env["project.project"].create(
            {"name": "Test project", "allow_timesheets": True}
        )
        self.analytic_account = self.project.analytic_account_id
        self.task = self.env["project.task"].create(
            {"name": "Test task", "project_id": self.project.id}
        )
        self.line = self.env["account.analytic.line"].create(
            {
                "date_time": datetime.now() - timedelta(hours=1),
                "task_id": self.task.id,
                "project_id": self.project.id,
                "account_id": self.analytic_account.id,
                "name": "Test line",
            }
        )

    def _create_wizard(self, action, active_record):
        """Create a new hr.timesheet.switch wizard in the specified context.

        :param dict action: Action definition that creates the wizard.
        :param active_record: Record being browsed when creating the wizard.
        """
        self.assertEqual(action["res_model"], "hr.timesheet.switch")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["view_type"], "form")
        return (
            active_record.env[action["res_model"]]
            .with_context(
                active_id=active_record.id,
                active_ids=active_record.ids,
                active_model=active_record._name,
                **action.get("context", {}),
            )
            .create({})
        )

    def test_no_user_error_access_right(self):
        start_action = self.task.button_start_work()
        wizard = self._create_wizard(start_action, self.task)
        self.assertIsNotNone(wizard.id)
