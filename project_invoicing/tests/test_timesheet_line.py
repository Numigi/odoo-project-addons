# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from .common import TestAnalyticLineBase


class TestTimesheetLine(TestAnalyticLineBase):

    @classmethod
    def setUpClass(cls):
        super(TestTimesheetLine, cls).setUpClass()
        cls.timesheet = cls.env['hr_timesheet_sheet.sheet'].create({
            'employee_id': cls.employee.id,
            'date_from': datetime.now(),
            'date_to': datetime.now() + relativedelta(days=7),
        })
        cls.line_1 = cls.create_timesheet_line(4)
        cls.line_2 = cls.create_timesheet_line(5)

    def test_01_show_on_project_invoicing_draft(self):
        self.assertFalse(self.line_1.show_on_project_invoicing)
        self.assertFalse(self.line_2.show_on_project_invoicing)

    def test_02_show_on_project_invoicing_confirmed(self):
        self.timesheet.action_timesheet_confirm()
        self.assertFalse(self.line_1.show_on_project_invoicing)
        self.assertFalse(self.line_2.show_on_project_invoicing)

    def test_03_show_on_project_invoicing_done(self):
        self.timesheet.action_timesheet_confirm()
        self.timesheet.action_timesheet_done()
        self.assertTrue(self.line_1.show_on_project_invoicing)
        self.assertTrue(self.line_2.show_on_project_invoicing)
