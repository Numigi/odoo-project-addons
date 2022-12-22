# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.http import route, request
from odoo.tools import frozendict
from odoo.addons.project.controllers.portal import CustomerPortal
from ..models.project_task import NO_DISPLAY_SUBTASKS


class CustomerPortal(CustomerPortal):
    @route(
        ["/my/tasks", "/my/tasks/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_tasks(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        groupby="project",
        **kw
    ):
        _setup_no_subtasks()
        return super().portal_my_tasks(
            page=page,
            date_begin=date_begin,
            date_end=date_end,
            sortby=sortby,
            filterby=filterby,
            search=search,
            search_in=search_in,
            groupby=groupby,
            **kw
        )

    def _prepare_portal_layout_values(self):
        _setup_no_subtasks()
        return super()._prepare_portal_layout_values()


def _setup_no_subtasks():
    new_context = {NO_DISPLAY_SUBTASKS: True}
    request.env.context = frozendict(request.env.context, **new_context)
