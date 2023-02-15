# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectWithType(models.Model):
    _inherit = 'project.project'

    type_id = fields.Many2one(tracking=True)
