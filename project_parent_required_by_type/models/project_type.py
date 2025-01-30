# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models, fields


class ProjectType(models.Model):
    _inherit = "project.type"

    is_project_parent_required = fields.Boolean(string="Is project parent required")
