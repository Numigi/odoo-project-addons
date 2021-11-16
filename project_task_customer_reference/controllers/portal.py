# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/gpl).

from odoo.addons.portal.controllers.portal import CustomerPortal as _Portal
from odoo.http import request, route
from odoo.exceptions import AccessError, MissingError


class Portal(_Portal):
    @route(
        ["/my/task/<int:task_id>/modify_reference"],
        type="http",
        auth="public",
        website=True,
    )
    def task_update_customer_reference(self, task_id, token=None, reference=None, **kw):
        task = _get_task(task_id, token)

        if task is None:
            return request.redirect("/my")
        try:
            task_sudo = self._document_check_access(
                "project.task", task.id, access_token=token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        task.customer_reference = reference

        url = task.get_portal_url()
        return request.redirect(url)


def _get_task(task_id, access_token):
    task = request.env["project.task"].sudo().search([("id", "=", task_id)], limit=1)
    return task
