# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class ProjectTaskTypeExternalMail(models.Model):
    _inherit = "project.task.type"

    external_mail = fields.Boolean()


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _track_template(self, changes):
        res = super(ProjectTask, self)._track_template(changes)
        test_task = self[0]
        if "stage_id" in res and test_task.stage_id.external_mail:
            res["stage_id"][-1]["subtype_id"] = self.env[
                "ir.model.data"
            ]._xmlid_to_res_id("mail.mt_comment")
        return res
