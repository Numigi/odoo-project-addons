# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class AnalyticLine(models.Model):
    """Prevent an analytic line with a task and analytic account that don't match."""

    _inherit = "account.analytic.line"

    origin_task_id = fields.Many2one(
        "project.task", "Origin Task", ondelete="restrict", index=True
    )

    @api.depends('task_id', 'task_id.project_id', 'origin_task_id',
                 'origin_task_id.project_id')
    def _compute_project_id(self):
        for line in self.filtered(lambda line: not line.project_id):
            if line.task_id.project_id:
                line.project_id = line.task_id.project_id
            if not line.task_id.project_id and line.origin_task_id.project_id:
                line.project_id = line.origin_task_id.project_id

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        new_args = []

        for arg in args:
            if (isinstance(arg, (list, tuple))
                    and len(arg) == 3
                    and arg[0] == 'origin_task_id'
                    and arg[1] == 'ilike'):
                raw_value = str(arg[2])
                value = raw_value.strip()
                record_id = False
                if value.isdigit():
                    record_id = int(value)
                else:
                    match = re.search(r'^\[?(\d+)\]', value)
                    if match:
                        record_id = int(match.group(1))
                if record_id:
                    new_args.append(('origin_task_id', '=', record_id))
                    continue
            new_args.append(arg)

        return super(AnalyticLine, self).search(new_args, offset, limit, order, count)

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

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(AnalyticLine, self).create(vals_list)

        for line in lines:
            if line.task_id:
                line.origin_task_id = line.task_id
        return lines

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
            lambda line: line.user_id
            and line.task_id
            and line.origin_task_id != line.task_id
        )
        for line in lines_to_update:
            line.task_id = line.origin_task_id
