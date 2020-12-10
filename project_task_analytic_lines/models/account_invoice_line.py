# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class InvoiceLine(models.Model):
    """Prevent posting an invoice line with a task and a project that dont match."""

    _inherit = "account.invoice.line"

    task_id = fields.Many2one("project.task", "Task", ondelete="restrict", index=True)

    @api.onchange("account_analytic_id")
    def _onchange_analytic_account_empty_task(self):
        if self.account_analytic_id != self.task_id.project_id.analytic_account_id:
            self.task_id = False

    def _check_task_matches_with_project(self):
        task_not_matching_project = (
            self.task_id
            and self.task_id.project_id.analytic_account_id != self.account_analytic_id
        )
        if task_not_matching_project:
            raise ValidationError(
                _(
                    "The task {task} is set on the invoice line {line}. "
                    "This task does not match the project ({project}) set on the line."
                ).format(
                    line=self.display_name,
                    task=self.task_id.display_name,
                    project=self.account_analytic_id.display_name,
                )
            )
