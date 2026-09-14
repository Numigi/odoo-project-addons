# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import pytest
from datetime import timedelta
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProjectWorksheet(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self._create_partner()
        self.project = self._create_project()
        self.task = self._create_task()
        self.employee = self._create_employee()
        self.worksheet = self._create_worksheet()
        self._create_worksheet_line()

    def _create_partner(self):
        return self.env["res.partner"].create({"name": "Test Client"})

    def _create_project(self):
        return self.env["project.project"].create({
            "name": "Test Project",
            "partner_id": self.partner.id,
        })

    def _create_task(self):
        return self.env["project.task"].create({
            "name": "Test Task",
            "project_id": self.project.id,
        })

    def _create_employee(self):
        return self.env["hr.employee"].create({"name": "Test Employee"})

    def _create_worksheet(self):
        return self.env["project.worksheet"].create({
            "project_id": self.project.id,
            "supervisor_id": self.employee.id,
            "date_start": fields.Date.today(),
            "date_end": fields.Date.today(),
        })

    def _create_worksheet_line(self):
        self.env["project.worksheet.line"].create({
            "worksheet_id": self.worksheet.id,
            "employee_id": self.employee.id,
            "task_id": self.task.id,
            "name": "Installation",
            "unit_amount": 5.0,
            "date": fields.Date.today(),
        })

    def test_worksheet_total_hours(self):
        assert self.worksheet.total_hours == 5.0

    def test_invalid_date_range_raises_error(self):
        with pytest.raises(ValidationError):
            self.worksheet.date_end = self.worksheet.date_start - timedelta(days=1)

    def test_submit_to_client_creates_timesheets(self):
        self.worksheet.action_send_to_client()
        assert len(self.worksheet.timesheet_ids) == 1

    def test_submit_to_client_updates_state(self):
        self.worksheet.action_send_to_client()
        assert self.worksheet.state == "pending"

    def test_submit_to_client_sets_date_sent(self):
        self.worksheet.action_send_to_client()
        assert self.worksheet.date_sent

    def test_manager_confirm_updates_state(self):
        self.worksheet.action_manager_confirm()
        assert self.worksheet.state == "confirmed"

    def test_manager_confirm_sets_date_approve(self):
        self.worksheet.action_manager_confirm()
        assert self.worksheet.date_approve

    def test_reminder_needed_when_delay_exceeded(self):
        self.worksheet.company_id.worksheet_reminder_delay = 2
        self.worksheet.date_sent = fields.Datetime.now() - timedelta(days=3)
        assert self.worksheet._is_reminder_needed()

    def test_reminder_not_needed_when_delay_respected(self):
        self.worksheet.company_id.worksheet_reminder_delay = 2
        self.worksheet.date_sent = fields.Datetime.now() - timedelta(days=1)
        assert not self.worksheet._is_reminder_needed()
