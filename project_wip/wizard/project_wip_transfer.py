# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectWipTransferWizard(models.TransientModel):
    """Wizard that allows to define a custom date to post the WIP transfer move."""

    _name = "project.wip.transfer"
    _description = "Project WIP To CGS Wizard"

    project_id = fields.Many2one("project.project", "Project")
    cgs_journal_id = fields.Many2one(
        related="project_id.type_id.cgs_journal_id", readonly=True
    )
    wip_account_id = fields.Many2one(
        related="project_id.type_id.wip_account_id", readonly=True
    )
    cgs_account_id = fields.Many2one(
        related="project_id.type_id.cgs_account_id", readonly=True
    )
    accounting_date = fields.Date(
        default=fields.Date.context_today,
        help="The selected date will be used for posting the journal entries "
        "when transfering amounts from WIP to CGS.",
    )
    costs_to_transfer = fields.Monetary()
    currency_id = fields.Many2one(
        "res.currency",
        "Currency",
        related="project_id.company_id.currency_id",
        readonly=True,
    )

    @api.onchange("project_id")
    def _onchange_project_compute_costs_to_transfer(self):
        self = self.with_context(force_company=self.env.user.company_id.id)
        has_wip_account = bool(self.wip_account_id)
        if has_wip_account:
            self.costs_to_transfer = sum(
                line.balance
                for line in self.project_id._get_posted_unreconciled_wip_lines()
            )

    def validate(self):
        self = self.with_context(force_company=self.env.user.company_id.id)
        return self.project_id.action_wip_to_cgs(self.accounting_date)
