# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectTaskMaterial(models.Model):

    _inherit = "project.task.material"

    def _run_procurements(self):
        if not self.project_id.estimation_mode_active:
            return super()._run_procurements()
