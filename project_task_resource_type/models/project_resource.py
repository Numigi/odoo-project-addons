# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProjectResource(models.Model):
    _name = "project.resource"
    _inherit = ["mail.thread"]
    _description = "Project Resource"

    name = fields.Char(string="Name")
