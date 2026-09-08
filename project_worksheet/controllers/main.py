# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http, _
from odoo.http import request


class ProjectWorksheetPortal(http.Controller):

    @http.route(
        ["/my/worksheet/<int:worksheet_id>/<string:access_token>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_worksheet_view(self, worksheet_id, access_token=None, **kw):
        # Render the worksheet portal view
        worksheet = self._get_worksheet(worksheet_id, access_token)
        return request.render(
            "project_worksheet.portal_worksheet_template",
            {"worksheet": worksheet, "error": kw.get("error")}
        )

    @http.route(
        ["/my/worksheet/<int:worksheet_id>/accept"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def portal_worksheet_accept(self, worksheet_id, access_token=None, **kw):
        worksheet = self._get_worksheet(worksheet_id, access_token)
        self._validate_acceptance(worksheet, kw.get("confirm_checkbox"))
        worksheet.action_client_confirm()
        self._log_client_confirmation(worksheet)
        return request.redirect(worksheet.get_portal_url())

    def _get_worksheet(self, worksheet_id, access_token):
        # Retrieve and validate worksheet access
        worksheet = request.env["project.worksheet"].sudo().browse(worksheet_id)
        self._check_worksheet_access(worksheet, access_token)
        return worksheet

    def _check_worksheet_access(self, worksheet, access_token):
        # Raise 404 if token is invalid or worksheet does not exist
        if not worksheet.exists() or worksheet.access_token != access_token:
            raise request.not_found()

    def _validate_acceptance(self, worksheet, confirm_checkbox):
        # Redirect back with error if the checkbox was not checked
        if not confirm_checkbox:
            error_url = worksheet.get_portal_url(query_string="&error=missing_confirmation")
            raise request.redirect(error_url)

    def _log_client_confirmation(self, worksheet):
        # Log the signature/confirmation footprint in the chatter
        client_ip = request.httprequest.remote_addr
        message = _("Worksheet approved by client from IP: %s") % client_ip
        worksheet.message_post(body=message)