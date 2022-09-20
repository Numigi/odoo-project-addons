# © 2022-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.onchange('project_id')
    def remove_milestone_task(self):
        if self.project_id.use_milestones:
            self.milestone_id = False
