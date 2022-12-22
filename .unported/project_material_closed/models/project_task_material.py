# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskMaterial(models.Model):

    _inherit = "project.task.material"

    closed = fields.Boolean(related="project_id.closed", store=True)
