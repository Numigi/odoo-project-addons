# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    is_outsourcing = fields.Boolean(related="purchase_id.is_outsourcing")

    def _get_outsourcing_analytic_account(self):
        return self.purchase_id.project_id.analytic_account_id

    def _get_outsourcing_task(self):
        return self.purchase_id.task_id

    @api.onchange("product_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        if self.is_outsourcing:
            self.account_analytic_id = self._get_outsourcing_analytic_account()
            self.task_id = self._get_outsourcing_task()
        return result
