# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTaskWithMinAndMaxHours(models.Model):
    """Add the fields min_hours and max_hours on tasks."""

    _inherit = 'project.project'

    min_hours = fields.Float('Minimum Planned Hours')
    max_hours = fields.Float('Maximum Planned Hours')
    planned_hours = fields.Float(string='Ideal Planned Hours')

    @api.one
    @api.constrains('planned_hours', 'min_hours', 'max_hours')
    def _check_description(self):
        # Case where planned_hours is different from 0 or None
        if self.planned_hours:
            if self.min_hours > self.planned_hours:
                raise ValidationError(
                    _("Min Hours must be lesser than the planned hours.")
                )
            elif self.max_hours < self.planned_hours:
                raise ValidationError(
                    _("Max Hours must be greater than the planned hours.")
                )
