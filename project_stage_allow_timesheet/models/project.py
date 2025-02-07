# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):

    _inherit = "project.project"

    allow_timesheets = fields.Boolean(
        related="stage_id.allow_timesheets",
        store=True,
    )
