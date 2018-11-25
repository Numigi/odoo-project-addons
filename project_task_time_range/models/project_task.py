# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTaskWithMinAndMaxHours(models.Model):
    """Add the fields min_hours and max_hours on tasks."""

    _inherit = 'project.task'

    min_hours = fields.Float('Minimum Planned Hours')
    max_hours = fields.Float('Maximum Planned Hours')


class ProjectTaskWithPlannedHoursRenamed(models.Model):
    """Rename `Initially Planned Hours` to `Ideal Planned Hours`."""

    _inherit = 'project.task'

    planned_hours = fields.Float(string='Ideal Planned Hours')


class ProjectTaskWithMinAndMaxConstraints(models.Model):
    """ Add constraints on min_hours and max_hours

    see TA#6155
    """
    _inherit = 'project.task'

    @api.one
    @api.constrains('planned_hours', 'min_hours', 'max_hours')
    def _check_description(self):
        if self.planned_hours > 0:
            if self.min_hours > self.planned_hours:
                raise ValidationError(
                    _("Min Hours must be lesser than the planned hours.")
                )
            elif self.max_hours < self.planned_hours:
                raise ValidationError(
                    _("Max Hours must be greater than the planned hours.")
                )
