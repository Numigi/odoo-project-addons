# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Invoice(models.Model):

    _inherit = "account.invoice"

    @api.model
    def _anglo_saxon_sale_move_lines(self, i_line):
        """Propagate the task to journal items."""
        result = super()._anglo_saxon_sale_move_lines(i_line)
        for vals in result:
            if vals.get("account_analytic_id"):
                vals["task_id"] = i_line.task_id.id
        return result
