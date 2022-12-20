# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskDescriptionTemplate(models.Model):

    _name = "project.task.description.template"
    _description = "Project Task Description Template"
    _order = "sequence"

    name = fields.Char(required=True)
    description = fields.Html()
    active = fields.Boolean(default=True)
    sequence = fields.Integer()
