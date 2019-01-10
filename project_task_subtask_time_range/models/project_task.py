# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTaskSubtaskHours(models.Model):
    """Add the fields min_hours and max_hours on tasks."""

    _inherit = 'project.task'

    @api.model
    def calculate_summed_time(self, field_name):
        return round(sum(self.child_ids.mapped(field_name)), 2)

    @api.one
    def compute_calculated_min_hours(self):
        self.calculated_min_hours = self.calculate_summed_time('min_hours')

    @api.one
    def compute_calculated_max_hours(self):
        self.calculated_max_hours = self.calculate_summed_time('max_hours')

    @api.one
    def compute_calculated_planned_hours(self):
        self.calculated_planned_hours = self.calculate_summed_time('planned_hours')

    calculated_min_hours = fields.Float('Calculated Min', compute='compute_calculated_min_hours')
    calculated_max_hours = fields.Float('Calculated Max', compute='compute_calculated_max_hours')
    calculated_planned_hours = fields.Float('Calculated Ideal', compute='compute_calculated_planned_hours')
