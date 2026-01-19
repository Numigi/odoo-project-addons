# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


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
        _logger.info("Project Estimation Exit: Start validation")
        ctx = dict(self.env.context)
        auto_assign_config = self.env["ir.config_parameter"].sudo().get_param(
            "stock_auto_assign_disabled.config", "off"
        )
        if auto_assign_config == 'all':
            ctx.update({
                'stock_auto_assign_disable': True,  # Force the auto assign disable
            })
        res = super(ProjectEstimationExit, self.with_context(ctx)).validate()
        self.with_context(ctx)._trigger_procurements()
        return res

    def _trigger_procurements(self):
        for line in self.project_id.material_line_ids:
            if line._should_generate_procurement():
                line._run_procurements()
