# Copyright 2023-today  Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request
from odoo.addons.hr_timesheet.controllers.portal import TimesheetCustomerPortal


class TimesheetPortalBlock(TimesheetCustomerPortal):
    """Block access to timesheet portal routes for portal users."""

    @http.route(['/my/timesheets', '/my/timesheets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_timesheets(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='none', **kw):
        """Block access to /my/timesheets route."""
        return request.render("http_routing.403")
