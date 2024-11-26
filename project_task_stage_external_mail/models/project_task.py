# Copyright 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _track_template(self, changes):
        """Override to customize the tracking template for stage_id changes."""
        res = super()._track_template(changes)
        if "stage_id" in res:
            task = self[0]
            if task.stage_id.external_mail:
                comment_subtype = self.env.ref("mail.mt_comment")
                res["stage_id"][-1]["subtype_id"] = comment_subtype.id
        return res
