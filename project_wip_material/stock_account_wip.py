# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class StockMove(models.Model):
    """Generate WIP journal entries for consumption moves."""

    _inherit = 'stock.move'

    def _is_consumption(self):
        return self.picking_code == 'consumption'

    def _is_consumption_return(self):
        return self.picking_code == 'consumption_return'

    def _generate_consumption_account_move(self):
        wip_account = self.project_id.project_type_id.wip_account_id
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        self._create_account_move_line(
            debit_account_id=wip_account, credit_account_id=acc_valuation, journal_id=journal_id)

    def _generate_consumption_return_account_move(self):
        wip_account = self.project_id.project_type_id.wip_account_id
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        self._create_account_move_line(
            debit_account_id=acc_valuation, credit_account_id=wip_account, journal_id=journal_id)

    def _account_entry_move(self):
        self.ensure_one()
        if self._is_consumption():
            self._generate_consumption_account_move()
        elif self._is_consumption_return():
            self._generate_consumption_return_account_move()
        else:
            super()._account_entry_move()
