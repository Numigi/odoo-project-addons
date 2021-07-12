# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, _


class ProjectEstimationEnter(models.TransientModel):

    _name = "project.estimation.enter"
    _description = "Project Estimation Mode Enter Wizard"

    project_id = fields.Many2one("project.project")

    def validate(self):
        self.project_id.estimation_mode_active = True
