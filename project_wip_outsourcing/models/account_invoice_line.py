# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    def _get_outsourcing_wip_account(self):
        self = self.with_context(force_company=self.company_id.id)
        return self.purchase_id.project_id.project_type_id.wip_account_id

    @api.onchange("product_id")
    def _onchange_product_id(self):
        result = super()._onchange_product_id()
        if self.is_outsourcing:
            wip_account = self._get_outsourcing_wip_account()
            if wip_account:
                self.account_id = wip_account
        return result
