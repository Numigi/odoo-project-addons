# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    remaining_budget = fields.Float(compute="_compute_remaining_budget")

    @api.depends()
    def _compute_remaining_budget(self):
        analytic_line = self.env["account.analytic.line"]
        for record in self:
            consumed = sum(analytic_line.search([("project_id", "=", record.id)]).mapped("unit_amount"))
            record.remaining_budget = record.planned_hours - consumed
