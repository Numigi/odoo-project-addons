# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
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


def is_planned_hours_not_none(func):
    """ Case where planned_hours is different from None to avoid comparing oranges and pandas
    Bare in mind we want to check the case where planned_hours is 0
    """
    def wrapper(self, *args, **kwargs):
        if self.planned_hours is not None:
            func(self, *args, **kwargs)
    return wrapper


def _is_testing(env):
    return getattr(threading.currentThread(), 'testing', False)


class ProjectTaskWithMinAndMaxConstraints(models.Model):
    """ Add constraints on min_hours and max_hours.
    """
    _inherit = 'project.task'
    hours_fields = ('planned_hours', 'min_hours', 'max_hours')

    @api.one
    @api.constrains('planned_hours', 'min_hours', 'max_hours')
    @is_planned_hours_not_none
    def _check_max_hours(self):
        """Verify that max hours are greater than min hours.

        This constraint breaks the standard behavior of Odoo.
        Therefore, to prevent breaking unit tests of other project related
        modules, the constraint is by default deactivated when testing.
        """
        if _is_testing(self.env) and not self._context.get('enable_task_max_hours_constraint'):
            return

        if self.max_hours < self.planned_hours:
            raise ValidationError(
                _("Max Hours must be greater than the planned hours.")
            )

    @api.one
    @api.constrains(*hours_fields)
    @is_planned_hours_not_none
    def _check_min_hours(self):
        if self.min_hours > self.planned_hours:
            raise ValidationError(
                _("Min Hours must be lesser than the planned hours.")
            )

    @api.one
    @api.constrains(*hours_fields)
    @is_planned_hours_not_none
    def _check_positive_hours(self):
        if any(h < 0 for h in [self.min_hours, self.planned_hours, self.max_hours]):
            raise ValidationError(
                _("Hours must be positive numbers.")
            )
