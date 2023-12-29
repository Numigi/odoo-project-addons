# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo.addons.report_aeroo.controllers.portal import Portal as _Portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request, route
from odoo.exceptions import AccessError, MissingError

SIGN_PAGE_TEMPLATE = "meeting_minutes_certificate.signature_portal_template"
CERTIFICATE_LIST_PAGE_TEMPLATE = (
    "meeting_minutes_certificate.certificate_list_portal_template"
)


TRAINING_CERTIFICATE_DOMAIN = [("certificate_enabled", "=", True)]


class Portal(_Portal):
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        minutes_count = request.env["meeting.minutes.project"].search_count(
            TRAINING_CERTIFICATE_DOMAIN
        )
        values["training_certificates_count"] = minutes_count
        return values

    @route(
        ["/my/training-certificates", "/my/training-certificates/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def training_certificate_list_page(self, page=1, **kw):
        minutes_obj = request.env["meeting.minutes.project"]

        total = minutes_obj.search_count(TRAINING_CERTIFICATE_DOMAIN)

        pager = portal_pager(
            url="/my/training-certificates",
            total=total,
            page=page,
            step=self._items_per_page,
        )

        minutes_list = minutes_obj.search(
            TRAINING_CERTIFICATE_DOMAIN,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        return request.render(
            CERTIFICATE_LIST_PAGE_TEMPLATE,
            {
                "page_name": "training_certificates",
                "minutes_list": minutes_list,
                "pager": pager,
            },
        )

    @route(
        ["/my/training-certificate/<int:task_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def training_certificate_page(self, task_id, access_token=None, **kw):
        minutes = _get_meeting_minutes(task_id, access_token)
        if minutes is None:
            return request.redirect("/my")

        signature = minutes._get_signature_line(request.env.user, access_token)

        return request.render(
            SIGN_PAGE_TEMPLATE,
            {
                "page_name": "training_certificate",
                "minutes": minutes,
                "signature": signature,
                "partner": signature.partner_id or request.env.user.partner_id,
            },
        )

    @route(
        ["/my/training-certificate/<int:task_id>/sign"],
        type="json",
        auth="public",
        website=True,
    )
    def training_certificate_sign(
        self, task_id, access_token=None, signature=None, **kw
    ):
        minutes = _get_meeting_minutes(task_id, access_token)
        if minutes is None:
            return request.redirect("/my")

        line = minutes._get_signature_line(request.env.user, access_token)
        line.sign(signature)

        return {
            "force_refresh": True,
            "redirect_url": line.get_access_url(),
        }

    @route(
        ["/my/training-certificate/<int:task_id>/report"],
        type="http",
        auth="public",
        website=True,
    )
    def training_certificate_report(
        self, task_id, access_token=None, download=False, **kw
    ):
        minutes = _get_meeting_minutes(task_id, access_token)
        if minutes is None:
            return request.redirect("/my")

        template = minutes.certificate_report_id
        return self._show_aeroo_report(
            record=minutes, template=template, download=download
        )


def _get_meeting_minutes(task_id, access_token):
    minutes = (
        request.env["meeting.minutes.project"]
        .sudo()
        .search([("task_id", "=", task_id)], limit=1)
    )
    return (
        minutes if minutes._is_user_authorized(request.env.user, access_token) else None
    )
