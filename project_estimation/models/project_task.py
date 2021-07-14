# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    estimation_mode_active = fields.Boolean(
        related="project_id.estimation_mode_active", store=True
    )
