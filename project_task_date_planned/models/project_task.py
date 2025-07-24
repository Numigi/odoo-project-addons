# -*- coding: utf-8 -*-
# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskWithPlannedDate(models.Model):

    _inherit = 'project.task'

    date_planned = fields.Date(
        'Planned Date', index=True, copy=False,
        tracking=True)
