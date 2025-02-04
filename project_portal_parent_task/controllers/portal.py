# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.project.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError, MissingError


class ProjectCustomerPortal(CustomerPortal):
    def _task_get_page_view_values(self, task, access_token, **kwargs):
        values = super(ProjectCustomerPortal, self)._task_get_page_view_values(
            task, access_token, **kwargs
        )
        try:
            parent_accessible = bool(
                task.parent_id.id
                and self._document_check_access("project.task", task.parent_id.id)
            )
        except (AccessError, MissingError):
            parent_accessible = False
        values["parent_accessible"] = parent_accessible
        return values
