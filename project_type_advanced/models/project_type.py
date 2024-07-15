# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectType(models.Model):

    _inherit = "project.type"
    _order = "sequence"

    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    color = fields.Integer(string="Color Index")
