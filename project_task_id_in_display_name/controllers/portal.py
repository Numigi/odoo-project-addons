# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import urllib.parse

from odoo import http
from odoo.addons.project.controllers.portal import CustomerPortal


class ProjectPortalWithSearchTaskByID(CustomerPortal):
    """Allow the portal user to find a task directly by the task id.

    If the task with the given id is found, the user is redirected to the task form.
    """

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_tasks(self, search=None, **kw):
        is_searching_by_task_id = isinstance(search, str) and search.strip().isdigit()

        if is_searching_by_task_id:
            task_id = search.strip()
            task = http.request.env['project.task'].search(
                [('id_string', '=', task_id)], limit=1)
            if task:
                query = urllib.parse.urlencode(dict(kw))
                redirect_url = '/my/task/{task_id}?{query}'.format(task_id=task.id, query=query)
                return http.request.redirect(redirect_url)

        return super().portal_my_tasks(search=search, **kw)
