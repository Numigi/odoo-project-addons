# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    no_analytic_lines = fields.Boolean(
        help="If checked, analytic lines will not be generated when posting this journal entry."
    )
