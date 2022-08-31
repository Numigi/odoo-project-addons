# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectWithType(models.Model):
    """Add the field project_type_id on projects."""

    _inherit = 'project.project'

    project_type_id = fields.Many2one(
        'project.type', 'Type', ondelete='restrict', index=True,
        tracking=True)
