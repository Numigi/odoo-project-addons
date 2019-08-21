# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    is_shop_supply = fields.Boolean()

    def create_analytic_lines(self):
        result = super().create_analytic_lines()

        shop_supply_lines = self.filtered(lambda l: l.is_shop_supply)
        shop_supply_lines.mapped('analytic_line_ids').write({'is_shop_supply': True})

        return result
