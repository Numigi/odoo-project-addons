# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    task_id = fields.Many2one(
        "project.task",
        string="Task",
        ondelete="restrict",
        index=True,
    )

    analytic_distribution_ids = fields.Many2many(
        "account.analytic.account",
        compute="_compute_analytic_distribution_ids",
        store=False,
        string="Analytic Distribution IDs",
    )

    @api.depends("analytic_distribution")
    def _compute_analytic_distribution_ids(self):
        for rec in self:
            if rec.analytic_distribution:
                rec.analytic_distribution_ids = [
                    (6, 0, list(map(int, rec.analytic_distribution.keys())))
                ]
            else:
                rec.analytic_distribution_ids = [(6, 0, [])]

    @api.onchange("analytic_distribution")
    def _onchange_analytic_account_empty_task(self):
        if self.task_id.project_id.analytic_account_id not in self.analytic_distribution.keys():
            self.task_id = False

    def _prepare_analytic_line(self):
        result = super(AccountMoveLine, self)._prepare_analytic_line()
        for vals in result:
            move_line = self.browse(vals["move_id"])
            vals["origin_task_id"] = move_line.task_id.id
        return result

    def _check_task_matches_with_project(self):
        task_not_matching_project = (
            self.task_id
            and self.task_id.project_id.analytic_account_id not in self.analytic_distribution.keys()
        )
        if task_not_matching_project:
            raise ValidationError(
                _(
                    "The task {task} is set on the invoice line {line}. "
                    "This task does not match the project ({project}) set on the line."
                ).format(
                    line=self.display_name,
                    task=self.task_id.display_name,
                    project=self.analytic_account_id.display_name,
                )
            )
