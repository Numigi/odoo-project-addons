# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectStage(models.Model):
    _inherit = 'project.project.stage'

    allow_timesheet = fields.Boolean(
        default=True,
    )
