# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.osv.expression import AND

NO_DISPLAY_SUBTASKS = "no_display_subtasks"


class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.model
    def _where_calc(self, domain, active_test=True):
        if self._context.get(NO_DISPLAY_SUBTASKS):
            domain = AND([domain or [], [("parent_id", "=", False)]])

        return super()._where_calc(domain, active_test)
