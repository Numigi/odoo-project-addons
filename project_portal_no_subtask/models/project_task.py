# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.osv.expression import AND

NO_DISPLAY_SUBTASKS = "no_display_subtasks"


class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        if self._context.get(NO_DISPLAY_SUBTASKS):
            args = AND([args or [], [("parent_id", "=", False)]])

        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
