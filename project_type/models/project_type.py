# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectType(models.Model):

    _inherit = 'project.type'
    _order = 'sequence'

    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color Index')
