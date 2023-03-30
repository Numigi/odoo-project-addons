# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    lump_sum = fields.Boolean(compute="_compute_lump_sum", store=True)

    @api.depends("project_id.lump_sum", "origin_task_id.project_id.lump_sum")
    def _compute_lump_sum(self):
        for line in self:
            line.lump_sum = (
                line.project_id.lump_sum
                if line.project_id
                else line.origin_task_id.project_id.lump_sum
            )
