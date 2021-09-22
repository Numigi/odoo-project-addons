# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProjectEstimationExit(models.TransientModel):

    _inherit = "project.estimation.exit"

    task_ids = fields.Many2many(
        "project.task", "project_estimation_exit_task_rel", "wizard_id", "task_id"
    )

    @api.onchange("project_id")
    def _set_tasks(self):
        self.task_ids = self.env["project.task"].search(
            [("project_id", "=", self.project_id.id)]
        )

    def validate(self):
        super().validate()
        self._trigger_procurements()

    def _trigger_procurements(self):
        for line in self.project_id.material_line_ids:
            if line._should_generate_procurement():
                line._run_procurements()
