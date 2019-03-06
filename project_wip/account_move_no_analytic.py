# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):

    _inherit = 'account.move'

    no_analytic_lines = fields.Boolean(
        help="If checked, analytic lines will not be generated when posting this journal entry."
    )


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    @api.multi
    def create_analytic_lines(self):
        """Prevent creating analytic lines for moves with no_analytic_lines checked."""
        lines_with_no_analytic = self.filtered(lambda l: l.move_id.no_analytic_lines)
        lines_with_analytic = self - lines_with_no_analytic

        if lines_with_no_analytic:
            # Remove analytic entries in case they were created before
            # checking no_analytic_lines.
            lines_with_no_analytic.mapped('analytic_line_ids').unlink()
            _logger.info(
                'No analytic line created for the account moves {}.'
                .format(lines_with_no_analytic.ids)
            )

        super(AccountMoveLine, lines_with_analytic).create_analytic_lines()
