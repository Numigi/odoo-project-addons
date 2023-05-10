# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectType(models.Model):
    """Add the salary account to project types."""

    _inherit = "project.type"

    salary_journal_id = fields.Many2one(
        "account.journal",
        "Salary Journal",
        company_dependent=True,
        help="Journal used for transfering salaries into work in progress "
        "when creating or updating a timesheet entry.",
    )

    salary_account_id = fields.Many2one(
        "account.account",
        "Salary Account",
        company_dependent=True,
        help="Account used for the salaries (usually the credit part) "
        "when transfering salaries into work in progress.",
    )

    @api.constrains("salary_account_id", "salary_journal_id", "wip_account_id")
    def _check_required_fields_for_salary_entries(self):
        self = self.with_context(force_company=self.env.user.company_id.id)
        project_types_with_salary_account = self.filtered(lambda t: t.salary_account_id)
        for project_type in project_types_with_salary_account:
            if not project_type.wip_account_id:
                raise ValidationError(
                    _(
                        "If the salary account is filled for a project type, "
                        "the work in progress account must be filled as well."
                    )
                )

            if not project_type.salary_journal_id:
                raise ValidationError(
                    _(
                        "If the salary account is filled for a project type, "
                        "the salary journal must be filled as well."
                    )
                )
