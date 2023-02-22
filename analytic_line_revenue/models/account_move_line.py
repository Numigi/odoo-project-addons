# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def create_analytic_lines(self):
        result = super().create_analytic_lines()

        revenue_lines = self.filtered(
            lambda l: l.account_id.user_type_id.internal_group == "income"
        )
        revenue_lines.mapped("analytic_line_ids").write({"revenue": True})

        return result
