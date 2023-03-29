# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AnalyticLine(models.Model):
    """Prevent an analytic line with a task and analytic account that don't match."""

    _inherit = "account.analytic.line"

    origin_task_id = fields.Many2one(
        "project.task", "Origin Task", ondelete="restrict", index=True
    )

    @api.onchange("account_id")
    def _onchange_analytic_account_empty_task(self):
        if self.account_id != self.origin_task_id.project_id.analytic_account_id:
            self.origin_task_id = False

    @api.constrains("origin_task_id", "account_id")
    def _check_origin_task_and_project_match(self):
        for line in self:
            task_not_matching_project = (
                    line.origin_task_id
                    and line.origin_task_id.project_id.analytic_account_id
                    != line.account_id
            )
            if task_not_matching_project:
                raise ValidationError(
                    _(
                        "The origin task {task} is set on the analytic line {line}. "
                        "This task does not match the analytic account ({analytic_account}) "
                        "set on the line."
                    ).format(
                        line=line.display_name,
                        task=line.origin_task_id.display_name,
                        analytic_account=line.account_id.display_name,
                    )
                )

    @api.model
    def create(self, vals):
        if vals.get("task_id"):
            vals["origin_task_id"] = vals["task_id"]
        return super(AnalyticLine, self).create(vals)

    def write(self, vals):
        if vals.get("task_id"):
            vals["origin_task_id"] = vals["task_id"]

        super(AnalyticLine, self).write(vals)

        if vals.get("origin_task_id"):
            self._propagate_origin_task_to_timesheet_lines()

        return True

    def _propagate_origin_task_to_timesheet_lines(self):
        """Backward propagation of origin_task_id to task_id.

        This allows the system to behave in a more transparent way
        when manually changing the value of origin_task_id
        for a timesheet line.
        """
        lines_to_update = self.filtered(
            lambda l: l.task_id and l.origin_task_id != l.task_id
        )
        for line in lines_to_update:
            line.task_id = line.origin_task_id
