# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Project(models.Model):

    _inherit = 'project.project'

    @api.onchange('project_type_id')
    def _on_change_project_type_id__set_default_task_stages(self):
        if self.project_type_id:
            self.type_ids = self.project_type_id.default_task_stage_ids
