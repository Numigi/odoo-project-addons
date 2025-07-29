# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    """Generate WIP journal entries for consumption moves."""

    _inherit = "stock.move"

    def _is_in(self):
        """Use the same valuation as incoming moves for consumption return."""
        return super()._is_in() or self._is_consumption_return()

    def _is_out(self):
        """Use the same valuation as outgoing moves for consumptions."""
        return super()._is_out() or self._is_consumption()

    def _account_entry_move(self, qty, description, svl_id, cost):
        """Accounting Valuation Entries"""
        self.ensure_one()
        if self.product_id.type != "product":
            # no stock valuation for consumable products
            return False
        if (
            self.restrict_partner_id
            and self.restrict_partner_id != self.company_id.partner_id
        ):
            # if the move isn't owned by the company, we don't make any valuation
            return False
        # add consumption logic
        if self._is_consumption():
            self._generate_consumption_account_move(qty, description, svl_id, cost)
        elif self._is_consumption_return():
            self._generate_consumption_return_account_move(
                qty, description, svl_id, cost
            )
        else:
            super()._account_entry_move(qty, description, svl_id, cost)

    def _prepare_account_move_line(
        self, qty, cost, credit_account_id, debit_account_id, description
    ):
        """Add the analytic to WIP account move lines."""
        self.ensure_one()
        move_line_vals = super()._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id, description
        )

        if self._is_consumption() or self._is_consumption_return():
            wip_account = self._get_wip_account()
            analytic_account = self._get_project_analytic_account()
            lines_with_wip_account = (
                line
                for line in move_line_vals
                if line[2]["account_id"] == wip_account.id
            )
            for line in lines_with_wip_account:
                line[2]["analytic_account_id"] = analytic_account.id
                line[2]["task_id"] = self.task_id.id

        return move_line_vals

    def _is_consumption(self):
        return self.picking_code == "consumption"

    def _is_consumption_return(self):
        return self.picking_code == "consumption_return"

    def _generate_consumption_account_move(self, qty, description, svl_id, cost):
        self._check_project_has_wip_account()
        wip_account = self._get_wip_account()
        journal_id, acc_src, acc_dest, acc_valuation = (
            self._get_accounting_data_for_valuation()
        )
        # Create Journal Entry for consuming products
        cost = -1 * cost
        self.with_company(self.project_id.company_id.id)._create_account_move_line(
            credit_account_id=acc_valuation,
            debit_account_id=wip_account.id,
            journal_id=journal_id,
            qty=qty,
            description=description,
            svl_id=svl_id,
            cost=cost,
        )

    def _generate_consumption_return_account_move(self, qty, description, svl_id, cost):
        self._check_project_has_wip_account()
        wip_account = self._get_wip_account()
        journal_id, acc_src, acc_dest, acc_valuation = (
            self._get_accounting_data_for_valuation()
        )
        # Create Journal Entry for products returning to the company;
        self.with_company(self.project_id.company_id.id)._create_account_move_line(
            credit_account_id=wip_account.id,
            debit_account_id=acc_valuation,
            journal_id=journal_id,
            qty=qty,
            description=description,
            svl_id=svl_id,
            cost=cost,
        )

    def _check_project_has_wip_account(self):
        self = self.with_company(self.company_id.id)
        project = self.project_id
        if not project.type_id:
            raise ValidationError(
                _(
                    "The transfer {picking} can not be processed because "
                    "the project {project} has no project type."
                ).format(
                    picking=self.picking_id.name,
                    project=project.display_name,
                )
            )

        if not project.type_id.wip_account_id:
            raise ValidationError(
                _(
                    "The transfer {picking} can not be processed because "
                    "the project type {project_type} has no WIP account."
                ).format(
                    picking=self.picking_id.name,
                    project_type=project.type_id.display_name,
                )
            )

    def _get_wip_account(self):
        self = self.with_company(self.company_id.id)
        return self.project_id.type_id.wip_account_id

    def _get_project_analytic_account(self):
        self = self.with_company(self.company_id.id)
        return self.project_id.analytic_account_id
