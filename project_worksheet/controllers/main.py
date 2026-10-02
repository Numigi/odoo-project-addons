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
        worksheet = self._get_worksheet(worksheet_id, access_token)
        backend_redirect = self._redirect_internal_user_to_backend(worksheet)
        if backend_redirect:
            return backend_redirect
        return request.render(
            "project_worksheet.portal_worksheet_template",
            {"worksheet": worksheet, "error": kw.get("error")}
        )

    def _redirect_internal_user_to_backend(self, worksheet):
        # The portal link shared with the client must not expose the client
        # portal page to internal Odoo users: send them to the backend form
        # instead (same behaviour as a sale order).
        user = request.env.user
        if user.has_group("base.group_user"):
            return request.redirect(self._get_backend_form_url(worksheet))
        return None

    def _get_backend_form_url(self, worksheet):
        return "/web#id=%s&model=%s&view_type=form" % (worksheet.id, worksheet._name)

    @http.route(
        ["/my/worksheet/<int:worksheet_id>/accept"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def portal_worksheet_accept(self, worksheet_id, access_token=None, **kw):
        worksheet = self._get_worksheet(worksheet_id, access_token)
        self._check_approval_access_rights(worksheet)
        self._validate_acceptance(worksheet, kw.get("confirm_checkbox"))
        worksheet.action_client_confirm()
        self._log_client_confirmation(worksheet)
        return request.redirect(worksheet.get_portal_url())

    def _get_worksheet(self, worksheet_id, access_token):
        worksheet = request.env["project.worksheet"].sudo().browse(worksheet_id)
        self._check_worksheet_access(worksheet, access_token)
        return worksheet

    def _check_worksheet_access(self, worksheet, access_token):
        if not worksheet.exists() or worksheet.access_token != access_token:
            raise request.not_found()

    def _check_approval_access_rights(self, worksheet):
        user = request.env.user
        if user.has_group("base.group_user"):
            self._check_manager_group(user, worksheet)

    def _check_manager_group(self, user, worksheet):
        if not user.has_group("project_worksheet.group_project_worksheet_manager"):
            self._redirect_unauthorized(worksheet)

    def _redirect_unauthorized(self, worksheet):
        error_url = worksheet.get_portal_url(query_string="&error=unauthorized")
        raise request.redirect(error_url)

    def _validate_acceptance(self, worksheet, confirm_checkbox):
        if not confirm_checkbox:
            self._redirect_missing_confirmation(worksheet)

    def _redirect_missing_confirmation(self, worksheet):
        error_url = worksheet.get_portal_url(query_string="&error=missing_confirmation")
        raise request.redirect(error_url)

    def _log_client_confirmation(self, worksheet):
        client_ip = request.httprequest.remote_addr
        message = _("Worksheet approved by client from IP: %s") % client_ip
        worksheet.message_post(body=message)
