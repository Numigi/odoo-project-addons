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

    @api.constrains("worksheet_id", "unit_amount", "task_id")
    def _check_locked_worksheet(self):
        # Prevent modification if the associated worksheet is approved
        locked_lines = (line for line in self if self._is_worksheet_approved(line))
        for _line in locked_lines:
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
