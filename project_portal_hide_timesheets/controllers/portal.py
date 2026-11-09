# Copyright 2023-today  Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request
from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal
from odoo.exceptions import AccessError


class TimesheetCustomerPortalHidden(TimesheetCustomerPortal):
    """Override portal controller to completely hide timesheets."""

    @http.route()
    def portal_my_timesheets(self, **kwargs):
        """Block access to timesheets portal page."""
        raise AccessError("Timesheets are not accessible through the portal.")

    def _show_task_report(self, task_id, report_type, download=False):
        """Block timesheet report generation."""
        raise AccessError("Timesheet reports are not accessible through the portal.")

    def _prepare_tasks_values(
        self,
        page,
        date_begin,
        date_end,
        sortby,
        search,
        search_in,
        groupby,
        url="/my/tasks",
        domain=None,
        su=False,
        project=False,
    ):
        """Override to remove timesheet-related values."""
        values = super()._prepare_tasks_values(
            page,
            date_begin,
            date_end,
            sortby,
            search,
            search_in,
            groupby,
            url,
            domain,
            su,
            project,
        )
        # Remove timesheet-related keys
        values.pop("is_uom_day", None)
        return values
