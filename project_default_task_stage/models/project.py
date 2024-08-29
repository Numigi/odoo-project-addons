# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Project(models.Model):

    _inherit = "project.project"

    @api.onchange("type_id")
    def _on_change_project_type_id__set_default_task_stages(self):
        if self.type_id:
            type_ids = self.type_id.default_task_stage_ids
            self.type_ids = [(6, 0, type_ids.ids)]
