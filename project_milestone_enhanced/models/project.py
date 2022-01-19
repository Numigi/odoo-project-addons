# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Project(models.Model):

    _inherit = "project.project"

    @api.multi
    def copy(self, vals=None):
        project = super().copy(vals)
        project._link_tasks_to_milestones()
        return project

    def _link_tasks_to_milestones(self):
        for task in self.task_ids.filtered("milestone_id"):
            task.milestone_id = self._find_equivalent_milestone(task.milestone_id)

    def _find_equivalent_milestone(self, milestone):
        return next((m for m in self.milestone_ids if m.name == milestone.name), None)
