# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    is_shop_supply = fields.Boolean()

    shop_supply_account_move_id = fields.Many2one(
        "account.move", "Shop Supply Entry", ondelete="restrict"
    )

    @api.model
    def create(self, vals):
        """On timesheet create, create or update the wip journal entry.

        Because the creation of a timesheet is complex, the journal entry
        may be created by a write before the return of super().create(vals).
        """
        line = super().create(vals)
        if line._requires_shop_supply_move() and \
                not line._context.get('shop_supply_move'):
            line.with_context(shop_supply_move=True).sudo()\
                ._create_update_or_reverse_shop_supply_move()
        return line

    @api.multi
    def write(self, vals):
        """When updating an analytic line, create / update / delete the wip entry.

        Whether the wip entry must be created / updated / deleted depends
        on which field is written to. This prevents an infinite loop.
        """
        super().write(vals)

        fields_to_check = self._get_shop_supply_move_dependent_fields()
        if fields_to_check.intersection(vals):
            for line in self:
                line.sudo()._create_update_or_reverse_shop_supply_move()

        return True

    @api.multi
    def unlink(self):
        """Reverse the salary account move entry when a timesheet line is deleted."""
        lines_with_moves = self.filtered(lambda l: l.shop_supply_account_move_id)
        for line in lines_with_moves:
            line.sudo()._reverse_shop_supply_account_move_for_deleted_timesheet()
        return super().unlink()

    def _create_update_or_reverse_shop_supply_move(self):
        """Create / Update / Reverse the wip account move.

        Depending on the status of the timesheet line,
        the wip move is either created, updated or reversed.
        """
        must_create_shop_supply_move = (
            self._requires_shop_supply_move() and not self.shop_supply_account_move_id
        )
        must_update_shop_supply_move = (
            self._requires_shop_supply_move() and self.shop_supply_account_move_id
        )
        must_reverse_shop_supply_move = (
            not self._requires_shop_supply_move() and self.shop_supply_account_move_id
        )

        if must_create_shop_supply_move:
            self._create_shop_supply_move()

        elif must_update_shop_supply_move:
            self._update_shop_supply_move()

        elif must_reverse_shop_supply_move:
            self._reverse_shop_supply_account_move_for_updated_timesheet()

    def _create_shop_supply_move(self):
        """Create the wip journal entry."""
        vals = self._get_shop_supply_move_vals()
        self.shop_supply_account_move_id = self.env["account.move"].create(vals)
        self.shop_supply_account_move_id.post()

    def _update_shop_supply_move(self):
        """Update the wip journal entry."""
        if self._is_shop_supply_account_move_reconciled():
            raise ValidationError(
                _(
                    "The timesheet line {description} can not "
                    "be updated because the shop supply entry ({move_name}) is already "
                    "transfered into the cost of goods sold."
                ).format(
                    description=self._get_wip_timesheet_line_description(),
                    move_name=self.shop_supply_account_move_id.name,
                )
            )

        self.shop_supply_account_move_id.state = "draft"
        vals = self._get_shop_supply_move_vals()
        self.shop_supply_account_move_id.write(vals)
        self.shop_supply_account_move_id.post()

    def _reverse_shop_supply_account_move_for_deleted_timesheet(self):
        """Reverse the wip journal entry in the context of a deleted timesheet."""
        if self._is_shop_supply_account_move_reconciled():
            raise ValidationError(
                _(
                    "The timesheet line {description} can not "
                    "be deleted because the shop supply entry ({move_name}) is already "
                    "transfered into the cost of goods sold."
                ).format(
                    description=self._get_wip_timesheet_line_description(),
                    move_name=self.shop_supply_account_move_id.name,
                )
            )
        self.shop_supply_account_move_id.reverse_moves()

    def _reverse_shop_supply_account_move_for_updated_timesheet(self):
        """Reverse the wip journal entry in the context of an updated timesheet."""
        if self._is_shop_supply_account_move_reconciled():
            raise ValidationError(
                _(
                    "The timesheet line {description} can not "
                    "be updated because the shop supply entry ({move_name}) would be "
                    "reversed. This journal entry was already transfered into "
                    "the cost of goods sold."
                ).format(
                    description=self._get_wip_timesheet_line_description(),
                    move_name=self.shop_supply_account_move_id.name,
                )
            )
        self.shop_supply_account_move_id.reverse_moves()
        self.shop_supply_account_move_id = False

    def _requires_shop_supply_move(self):
        """Evaluate whether the timesheet line requires a shop supply entry.

        The shop supply account must be defined on the project type and
        as well as the shop supply rate.

        :rtype: bool
        """
        return (
            self._get_shop_supply_amount()
            and bool(self._get_shop_supply_account())
            and self._get_shop_supply_rate()
        )

    def _get_shop_supply_wip_move_line_vals(self):
        """Get the values for the wip move line (usually the debit).

        :rtype: dict
        """
        amount = self._get_shop_supply_amount()
        return {
            "account_id": self._get_wip_account().id,
            "name": self.name,
            "debit": amount if amount > 0 else 0,
            "credit": -amount if amount < 0 else 0,
            "quantity": self.unit_amount,
            "analytic_account_id": self.project_id.analytic_account_id.id,
            "is_shop_supply": True,
            "task_id": self.task_id.id,
        }

    def _get_shop_supply_move_line_vals(self):
        """Get the values for the shop supply move line (usually the credit).

        :rtype: dict
        """
        amount = self._get_shop_supply_amount()
        return {
            "account_id": self._get_shop_supply_account().id,
            "name": self.name,
            "debit": -amount if amount < 0 else 0,
            "credit": amount if amount > 0 else 0,
            "quantity": self.unit_amount,
        }

    def _get_shop_supply_amount(self):
        """Get the debit/credit amount for the shop supply entry.

        :rtype: float
        """
        return self.unit_amount * self._get_shop_supply_rate()

    def _get_shop_supply_move_vals(self):
        """Get the values for the wip account move.

        :rtype: dict
        """
        return {
            "company_id": self.company_id.id,
            "journal_id": self._get_shop_supply_journal().id,
            "date": self.date,
            "no_analytic_lines": False,
            "ref": self._get_shop_supply_move_reference(),
            "line_ids": [
                (5, 0),
                (0, 0, self._get_shop_supply_wip_move_line_vals()),
                (0, 0, self._get_shop_supply_move_line_vals()),
            ],
        }

    def _get_shop_supply_move_reference(self):
        return _("{project} / TA#{task} (Shop Supply)").format(
            project=self.project_id.display_name, task=self.task_id.id
        )

    def _is_shop_supply_account_move_reconciled(self):
        """Evaluate whether the wip journal entry is reconciled or not.

        :rtype: bool
        """
        return any(l.reconciled for l in self.shop_supply_account_move_id.line_ids)

    def _get_shop_supply_move_dependent_fields(self):
        """Get the fields that trigger an update of the wip entry.

        :rtype: Set
        """
        return {"name", "unit_amount", "date", "project_id", "task_id"}

    def _get_shop_supply_journal(self):
        return self.project_id.project_type_id.shop_supply_journal_id

    def _get_shop_supply_account(self):
        return self.project_id.project_type_id.shop_supply_account_id

    def _get_shop_supply_rate(self):
        return self.project_id.project_type_id.shop_supply_rate
