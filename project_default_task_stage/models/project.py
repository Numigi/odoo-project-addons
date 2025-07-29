# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Project(models.Model):

    _inherit = 'project.project'

    @api.onchange('type_id')
    def _on_change_project_type_id__set_default_task_stages(self):
        if self.type_id:
            self.type_ids = self.type_id.default_task_stage_ids
