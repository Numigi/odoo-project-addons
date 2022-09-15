# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectMilestoneType(models.Model):
    _name = "project.milestone.type"
    _description = "Milestone Types"

    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    active = fields.Boolean('Active', default=True)

