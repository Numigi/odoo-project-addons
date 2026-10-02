# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    worksheet_id = fields.Many2one(
        comodel_name="project.worksheet",
        string="Worksheet",
        ondelete="set null",
        help="Worksheet associated with this timesheet entry.",
    )

    @api.constrains("worksheet_id", "unit_amount", "task_id", "date", "employee_id", "name")
    def _check_locked_worksheet(self):
        if self._is_worksheet_lock_bypassed():
            return
        for line in self:
            line._validate_not_linked_to_worksheet()

    def _is_worksheet_lock_bypassed(self):
        # Verify if the action is triggered internally by the worksheet synchronization
        return self.env.context.get("bypass_worksheet_lock")

    def _validate_not_linked_to_worksheet(self):
        if self.worksheet_id:
            self._raise_locked_worksheet_error()

    def _is_worksheet_approved(self, line):
        # Return true if the worksheet is in approved state
        if not line.worksheet_id:
            return False
        return line.worksheet_id.state == "approved"

    def _raise_locked_worksheet_error(self):
        # Centralized exception raising for locked worksheets
        raise UserError(
            _("You cannot modify timesheets linked to an approved worksheet.")
        )

    def unlink(self):
        if not self._is_worksheet_lock_bypassed():
            self._check_unlink_conditions()
        return super().unlink()

    def _check_unlink_conditions(self):
        for line in self:
            line._validate_unlink_allowed()

    def _validate_unlink_allowed(self):
        if self.worksheet_id:
            self._raise_unlink_linked_line_error()

    def _raise_unlink_linked_line_error(self):
        raise UserError(
            "You cannot delete a timesheet line linked to a worksheet."
        )

