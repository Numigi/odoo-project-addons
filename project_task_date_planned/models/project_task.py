# -*- coding: utf-8 -*-
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskWithPlannedDate(models.Model):

    _inherit = 'project.task'

    date_planned = fields.Date(
        'Planned Date', index=True, copy=False,
        tracking=True)
