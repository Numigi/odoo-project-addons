# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTask(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        context = dict(
            cls.env.context, enable_project_stage_allow_timesheet_constraint=True
        )
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Employee"}
        )
        cls.env = cls.env(context=context)
        cls.project_stage_timesheet = cls.env["project.project.stage"].create(
            {"name": "project_stage", "allow_timesheet": True}
        )
        cls.project_stage_no_timesheet = cls.env["project.project.stage"].create(
            {"name": "project_stage_no_timesheet", "allow_timesheet": False}
        )
        cls.project_timesheet = cls.env["project.project"].create(
            {"name": "tproject", "stage_id": cls.project_stage_timesheet.id}
        )

        cls.project_no_timesheet = cls.env["project.project"].create(
            {"name": "tproject_no", "stage_id": cls.project_stage_no_timesheet.id}
        )

        cls.task_no_timesheet = cls.env["project.task"].create(
            {"name": "tTask_no", "project_id": cls.project_no_timesheet.id}
        )
        cls.task_timesheet = cls.env["project.task"].create(
            {"name": "tTask_no", "project_id": cls.project_timesheet.id}
        )

        cls.account_analytic_line = cls.env["account.analytic.line"].create(
            {
                "name": "line",
                "task_id": cls.task_timesheet.id,
                "project_id": cls.project_timesheet.id,
                "employee_id": cls.employee.id
            }
        )

    def test_whenTaskWithTimeSheetIsSetToProjectNoTimeSheet_thenRaiseError(self):
        with self.assertRaises(ValidationError):
            self.task_timesheet.project_id = self.project_no_timesheet

    def test_whenAALMovedToProjectNoTimeSheet_thenRaiseError(self):
        with self.assertRaises(ValidationError):
            self.task_timesheet.project_id = self.project_no_timesheet.id
