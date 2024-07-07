# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTaskWithPlannedDate(models.Model):

    _inherit = "project.task"

    date_planned = fields.Date("Planned Date", index=True, copy=False, tracking=True)
