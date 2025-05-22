# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    root_analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Root Analytic Account",
        compute="_compute_root_analytic_account_id",
        store=True,
    )

    @api.depends(
        "project_id",
        "project_id.analytic_account_id",
        "project_id.analytic_account_id.parent_id",
    )
    def _compute_root_analytic_account_id(self):
        for line in self:
            line.root_analytic_account_id = (
                line.project_id.analytic_account_id.parent_id
                if line.project_id and line.project_id.analytic_account_id
                else False
            )
