# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    def create_analytic_lines(self):
        result = super().create_analytic_lines()

        revenue_type = self.env.ref('account.data_account_type_revenue')
        revenue_lines = self.filtered(
            lambda l: l.account_id.user_type_id == revenue_type)
        revenue_lines.mapped('analytic_line_ids').write({'revenue': True})

        return result
