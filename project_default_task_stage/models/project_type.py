# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectType(models.Model):

    _inherit = "project.type"

    default_task_stage_ids = fields.Many2many(
        "project.task.type",
        "project_type_default_task_stage_rel",
        "type_id",
        "task_stage_id",
        string="Default Task Stages",
    )
