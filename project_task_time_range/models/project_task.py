# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskWithMinAndMaxHours(models.Model):
    """Add the fields min_hours and max_hours on tasks."""

    _inherit = 'project.task'

    min_hours = fields.Float('Minimum Planned Hours')
    max_hours = fields.Float('Maximum Planned Hours')


class ProjectTaskWithPlannedHoursRenamed(models.Model):
    """Rename `Initially Planned Hours` to `Ideal Planned Hours`."""

    _inherit = 'project.task'

    planned_hours = fields.Float(string='Ideal Planned Hours')
