# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        task = super().create(vals)
        # If milestone is set, propagate its target_date to the date_deadline of task
        if task.milestone_id:
            task.date_deadline = task.milestone_id.target_date
        return task

    @api.onchange("milestone_id")
    def _onchange_milestone_propagate_target_date(self):
        # Change to milestone target_date if its set on task
        # If milestone was removed, date_deadline will be set to project date
        if self.milestone_id:
            self.date_deadline = self.milestone_id.target_date
        elif self.project_id:
            self.date_deadline = self.project_id.date
