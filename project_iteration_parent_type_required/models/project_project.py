# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models, fields


class ProjectParentRequired(models.Model):
    _inherit = "project.project"

    # Create the join between the modules project_type and project_iteration
    is_parent_required = fields.Boolean(
        related="type_id.is_project_parent_required"
    )
