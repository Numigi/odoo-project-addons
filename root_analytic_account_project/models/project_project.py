# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    root_analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Root Analytic Account",
        compute="_compute_root_analytic_account_id",
        store=True,
    )

    @api.depends("analytic_account_id", "analytic_account_id.parent_id")
    def _compute_root_analytic_account_id(self):
        for project in self:
            analytic_account = project.analytic_account_id
            project.root_analytic_account_id = (
                analytic_account.parent_id
                if analytic_account and analytic_account.parent_id
                else False
            )
