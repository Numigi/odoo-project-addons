# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError


class ProjectType(models.Model):
    _inherit = "project.type"

    cgs_journal_id = fields.Many2one(
        "account.journal",
        "WIP To CGS Journal",
        company_dependent=True,
        help="Accounting journal used when transfering WIP journal items into CGS.",
    )
    wip_account_id = fields.Many2one(
        "account.account",
        "WIP Account",
        company_dependent=True,
        help="Account used to cumulate Work In Progress for this project type.",
    )
    cgs_account_id = fields.Many2one(
        "account.account",
        "CGS Account",
        company_dependent=True,
        help="Account used to cumulate Costs of Goods Sold for this project type.",
    )

    @api.constrains("wip_account_id")
    def _check_wip_account_allows_reconcile(self):
        """Check that the wip account on project type allows reconciliation."""
        self = self.with_company(self.env.user.company_id)
        project_types_with_wip_accounts = self.filtered(lambda t: t.wip_account_id)
        for project_type in project_types_with_wip_accounts:
            if not project_type.wip_account_id.reconcile:
                raise ValidationError(
                    _(
                        "The selected WIP account ({}) must allow reconciliation."
                    ).format(project_type.wip_account_id.display_name)
                )
