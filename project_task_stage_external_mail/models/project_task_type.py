# Copyright 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    external_mail = fields.Boolean()
