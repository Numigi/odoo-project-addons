# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    closed = fields.Boolean(
        help="Tasks in this stage are considered closed.",
        default=False,
    )
