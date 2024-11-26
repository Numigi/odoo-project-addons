# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = "project.task"

    resource_id = fields.Many2one("project.resource")
