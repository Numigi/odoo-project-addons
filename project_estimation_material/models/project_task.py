# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.multi
    def copy(self, vals=None):
        task = super().copy(vals)

        if task.estimation_mode_active:
            task._copy_material_lines_from(self)

        return task

    def _copy_material_lines_from(self, task):
        for line in task.material_line_ids:
            line.copy({"task_id": self.id})
