# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectType(models.Model):

    _name = 'project.type'
    _description = 'Project Type'
    _order = 'sequence'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer()
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color Index')
