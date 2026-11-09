# Copyright 2023-today  Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _compute_allow_timesheets(self):
        """Override to force allow_timesheets to False for portal users."""
        portal_tasks = self.filtered(
            lambda t: self.env.user.has_group("base.group_portal")
        )
        portal_tasks.allow_timesheets = False
        super(ProjectTask, self - portal_tasks)._compute_allow_timesheets()
