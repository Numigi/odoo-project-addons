# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    task_id = fields.Many2one("project.task", "Task",
                              ondelete="restrict", index=True)

    @api.onchange("analytic_account_id")
    def _onchange_analytic_account_empty_task(self):
        if self.analytic_account_id != self.task_id.project_id.analytic_account_id:
            self.task_id = False

    def _prepare_analytic_line(self):
        result = super()._prepare_analytic_line()
        for vals in result:
            line = self.browse(vals["move_id"])
            vals["origin_task_id"] = line.task_id.id
        return result

    def _check_task_matches_with_project(self):
        task_not_matching_project = (
            self.task_id
            and self.task_id.project_id.analytic_account_id != self.analytic_account_id
        )
        if task_not_matching_project:
            raise ValidationError(
                _(
                    "The task {task} is set on the journal item {line}. "
                    "This task does not match the project ({project}) set on the line."
                ).format(
                    line=self.display_name,
                    task=self.task_id.display_name,
                    project=self.analytic_account_id.display_name,
                )
            )
