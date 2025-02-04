# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        for line in self.mapped("invoice_line_ids"):
            line._check_task_matches_with_project()
        return super(AccountMove, self).action_post()
