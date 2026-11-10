# Copyright 2023-today  Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request
from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal


class TimesheetPortalBlock(TimesheetCustomerPortal):
    """Block access to timesheet portal routes for portal users."""

    @http.route()
    def portal_my_timesheets(self, *args, **kwargs):
        """Block access to /my/timesheets route."""
        return request.render("website.403")
