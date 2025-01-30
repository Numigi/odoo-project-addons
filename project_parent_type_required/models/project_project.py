# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models, fields


class Project(models.Model):
    _inherit = "project.project"

    is_parent_required = fields.Boolean(related="type_id.is_project_parent_required")
