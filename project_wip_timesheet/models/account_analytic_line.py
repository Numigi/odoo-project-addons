# © 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TimesheetLine(models.Model):

    _inherit = "account.analytic.line"

    salary_account_move_id = fields.Many2one(
        "account.move", "Salary Journal Entry", ondelete="restrict"
    )

    @api.model
    def create(self, vals):
        """On timesheet create, create or update the wip journal entry.

        Because the creation of a timesheet is complex, the journal entry
        may be created by a write before the return of super().create(vals).
        """
        line = super().create(vals)
        if line._requires_salary_move():
            line.sudo()._create_update_or_reverse_salary_account_move()
        return line

    def write(self, vals):
        """When updating an analytic line, create / update / delete the wip entry.

        Whether the wip entry must be created / updated / deleted depends
        on which field is written to. This prevents an infinite loop.
        """
        super().write(vals)

        fields_to_check = self._get_salary_move_dependent_fields()
        if fields_to_check.intersection(vals):
            for line in self:
                line.sudo()._create_update_or_reverse_salary_account_move()

        return True

    def unlink(self):
        """Reverse the salary account move entry when a timesheet line is deleted."""
        lines_with_moves = self.filtered(lambda line: line.salary_account_move_id)
        for line in lines_with_moves:
            line.sudo()._reverse_salary_account_move_for_deleted_timesheet()
        return super().unlink()

    def _create_update_or_reverse_salary_account_move(self):
        """Create / Update / Reverse the wip account move.

        Depending on the status of the timesheet line,
        the wip move is either created, updated or reversed.
        """
        must_create_salary_move = (
            self._requires_salary_move() and not self.salary_account_move_id
        )
        must_update_salary_move = (
            self._requires_salary_move() and self.salary_account_move_id
        )
        must_reverse_salary_move = (
            not self._requires_salary_move() and self.salary_account_move_id
        )

        if must_create_salary_move:
            self._create_salary_account_move()

        elif must_update_salary_move:
            self._update_salary_account_move()

        elif must_reverse_salary_move:
            self._reverse_salary_account_move_for_updated_timesheet()

    def _create_salary_account_move(self):
        """Create the wip journal entry."""
        vals = self._get_salary_account_move_vals()
        self.salary_account_move_id = self.env["account.move"].create(vals)
        self.salary_account_move_id.post()

    def _update_salary_account_move(self):
        """Update the wip journal entry."""
        if self._is_salary_account_move_reconciled():
            raise ValidationError(
                _(
                    "The timesheet line {description} can not "
                    "be updated because the work in progress entry ({move_name}) is already "
                    "transfered into the cost of goods sold."
                ).format(
                    description=self._get_wip_timesheet_line_description(),
                    move_name=self.salary_account_move_id.name,
                )
            )

        self.salary_account_move_id.state = "draft"
        vals = self._get_salary_account_move_vals()
        self.salary_account_move_id.write(vals)
        self.salary_account_move_id.post()

    def _reverse_salary_account_move_for_updated_timesheet(self):
        """Reverse the wip journal entry in the context of an updated timesheet."""
        if self._is_salary_account_move_reconciled():
            raise ValidationError(
                _(
                    "The timesheet line {description} can not "
                    "be updated because the work in progress entry ({move_name}) would be "
                    "reversed. This journal entry was already transfered into "
                    "the cost of goods sold."
                ).format(
                    description=self._get_wip_timesheet_line_description(),
                    move_name=self.salary_account_move_id.name,
                )
            )
        self.salary_account_move_id._reverse_moves()

        self.salary_account_move_id = False

    def _reverse_salary_account_move_for_deleted_timesheet(self):
        """Reverse the wip journal entry in the context of a deleted timesheet."""
        if self._is_salary_account_move_reconciled():
            raise ValidationError(
                _(
                    "The timesheet line {description} can not "
                    "be deleted because the work in progress entry ({move_name}) is already "
                    "transfered into the cost of goods sold."
                ).format(
                    description=self._get_wip_timesheet_line_description(),
                    move_name=self.salary_account_move_id.name,
                )
            )
        self.salary_account_move_id._reverse_moves()

    def _is_salary_account_move_reconciled(self):
        return any(line.reconciled for line in self.salary_account_move_id.line_ids)

    def _get_salary_account_move_vals(self):
        """Get the values for the wip account move.

        :rtype: dict
        """
        reference = "{project} / TA#{task}".format(
            project=self.project_id.display_name, task=self.task_id.id
        )
        return {
            "company_id": self.company_id.id,
            "journal_id": self._get_salary_journal().id,
            "date": self.date,
            "no_analytic_lines": True,
            "ref": reference,
            "line_ids": [
                (5, 0),
                (0, 0, self._get_salary_wip_move_line_vals()),
                (0, 0, self._get_salary_move_line_vals()),
            ],
        }

    def _get_salary_wip_move_line_vals(self):
        """Get the values for the wip account move line (usually the debit).

        :rtype: dict
        """
        return {
            "account_id": self._get_wip_account().id,
            "name": self.name,
            "debit": -self.amount if self.amount < 0 else 0,
            "credit": self.amount if self.amount > 0 else 0,
            "quantity": self.unit_amount,
            "analytic_account_id": self.project_id.analytic_account_id.id,
            "task_id": self.task_id.id,
        }

    def _get_salary_move_line_vals(self):
        """Get the values for the salary account move line (usually the credit).

        :rtype: dict
        """
        return {
            "account_id": self._get_salary_account().id,
            "name": self.name,
            "debit": self.amount if self.amount > 0 else 0,
            "credit": -self.amount if self.amount < 0 else 0,
            "quantity": self.unit_amount,
        }

    def _get_salary_move_dependent_fields(self):
        """Get the fields that trigger an update of the wip entry.

        :rtype: Set
        """
        return {"name", "amount", "unit_amount", "date", "project_id", "task_id"}

    def _requires_salary_move(self):
        """Evaluate whether the timesheet line requires a wip journal entry.

        If the account.analytic.line has a value in the field project_id,
        it is a timesheet line.

        If the project type has a salary account, then the line requires
        a salary account move.

        :rtype: bool
        """
        return self.amount and bool(self._get_salary_account())

    def _get_salary_journal(self):
        """Get the journal to use for wip entry.

        :rtype: account.journal
        """
        self = self.with_context(force_company=self.company_id.id)
        return self.project_id.type_id.salary_journal_id

    def _get_salary_account(self):
        """Get the account to use for the salary move line.

        :rtype: account.account
        """
        return self.project_id.type_id.salary_account_id
