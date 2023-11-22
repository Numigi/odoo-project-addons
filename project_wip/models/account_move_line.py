# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def create_analytic_lines(self):
        """Prevent creating analytic lines for moves with no_analytic_lines checked."""
        lines_with_no_analytic = self.filtered(lambda l: l.move_id.no_analytic_lines)
        lines_with_analytic = self - lines_with_no_analytic

        if lines_with_no_analytic:
            # Remove analytic entries in case they were created before
            # checking no_analytic_lines.
            lines_with_no_analytic.mapped("analytic_line_ids").unlink()

        super(AccountMoveLine, lines_with_analytic).create_analytic_lines()
