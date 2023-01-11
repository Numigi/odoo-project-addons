# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, api, fields, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    @api.constrains('start_date')
    def _check_start_date_and_dependencies_end_date(self):
        sorted_child_ids = self.child_ids.sorted(
            key='target_date', reverse=True)
        child_last_end_dates = self.child_ids.sorted(
            key='target_date', reverse=True).mapped('target_date')
        if child_last_end_dates and self.start_date and \
                self.start_date < child_last_end_dates[0]:
            raise ValidationError(
                _('The milestone %s - %s is dependent on this '
                  'milestone and has a %s end date.'
                  % (sorted_child_ids[0].name,
                     sorted_child_ids[0].project_id.name,
                     fields.Date.to_string(child_last_end_dates[0]))
                  )
            )

    def _check_child_milestones_target_date(self, milestone):
        child_last_end_dates = milestone.child_ids.sorted(
            key='target_date', reverse=True).mapped('target_date')
        if child_last_end_dates and \
                (not milestone.start_date or milestone.start_date <= \
                    child_last_end_dates[0]):
                milestone_duration = \
                    milestone.target_date - milestone.start_date
                milestone.start_date = \
                    child_last_end_dates[0] + timedelta(days=1)
                milestone.target_date = \
                    milestone.start_date + milestone_duration

    def _get_parent_milestone(self, milestone):
        self._cr.execute(
            'SELECT milestone_id '
            'FROM "rel_project_milestone_dependencies"'
            ' WHERE child_id=%s' % milestone.id)
        milestone_id = self._cr.fetchone()
        return self.env['project.milestone'].browse(milestone_id[0]) \
            if milestone_id else None

    @api.multi
    def write(self, vals):
        for milestone in self:
            res = super(ProjectMilestone, milestone).write(vals)
            if 'child_ids' in vals:
                self._check_child_milestones_target_date(milestone)
            if 'target_date' in vals:
                parent_milestone = self._get_parent_milestone(milestone)
                if parent_milestone:
                    self._check_child_milestones_target_date(parent_milestone)
            return res
