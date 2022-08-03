# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    active_toggle = fields.Boolean(string="Toggle active", default=True)

    def toggle_active(self):
        res = super(AccountAnalyticAccount, self).toggle_active()
        self.toggle_active_change()
        return res

    def toggle_active_change(self):
        for account in self:
            account.active_toggle = account.active

    def write(self, vals):
        res = super(AccountAnalyticAccount, self).write(vals)
        if "active" in vals and vals["active"]:
            self._account_analytic_not_active()
        return res

    def _account_analytic_not_active(self):
        self.filtered(
            lambda account: not account.active_toggle).write({"active": False})
