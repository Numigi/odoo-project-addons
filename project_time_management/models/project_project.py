# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectTaskWithMinAndMaxHours(models.Model):
    """Add the fields min_hours and max_hours on tasks."""

    _inherit = 'project.project'

    @api.multi
    def get_parent_tasks(self):
        """ Return all the task without any parent.
        """
        # cannot use self.task_ids as task_ids exclude all the tasks in a
        # stage that is folded by default
        project_tasks = self.env['project.task'].search([['project_id', '=', self.id]])
        return project_tasks.filtered(lambda t: not t.parent_id)

    def calculate_sumed_time(self, field_name):
        return round(sum(self.get_parent_tasks().mapped(field_name)), 2)

    def compute_calculated_min_hours(self):
        for record in self:
            record.calculated_min_hours = record.calculate_sumed_time('min_hours')

    def compute_calculated_max_hours(self):
        for record in self:
            record.calculated_max_hours = record.calculate_sumed_time('max_hours')

    def compute_calculated_planned_hours(self):
        for record in self:
            record.calculated_planned_hours = record.calculate_sumed_time('planned_hours')

    def compute_calculated_remaining_hours(self):
        for record in self:
            record.calculated_remaining_hours = record.calculate_sumed_time('remaining_hours')

    def compute_calculated_effective_hours(self):
        for record in self:
            record.calculated_effective_hours = record.calculate_sumed_time('effective_hours')

    calculated_min_hours = fields.Float('Calculated Min', compute='compute_calculated_min_hours')
    calculated_max_hours = fields.Float('Calculated Max', compute='compute_calculated_max_hours')
    calculated_planned_hours = fields.Float('Calculated Ideal', compute='compute_calculated_planned_hours')
    calculated_remaining_hours = fields.Float(
        'Calculated Remaining Hours', compute='compute_calculated_remaining_hours'
    )
    calculated_effective_hours = fields.Float(
        'Calculated Effective Hours', compute='compute_calculated_effective_hours'
    )
