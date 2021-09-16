# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectEstimationExit(models.TransientModel):

    _name = "project.estimation.exit"
    _description = "Project Estimation Mode Exit Wizard"

    project_id = fields.Many2one("project.project")

    def validate(self):
        self.project_id.estimation_mode_active = False
