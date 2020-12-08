# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):

    _inherit = "account.move"

    @api.multi
    def post(self, invoice=False):
        for line in self.mapped("line_ids"):
            line._check_task_matches_with_project()

        return super().post(invoice)
