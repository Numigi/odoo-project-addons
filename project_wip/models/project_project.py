# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError, AccessError


class Project(models.Model):

    _inherit = "project.project"

    @api.multi
    def action_wip_to_cgs(self, accounting_date=None):
        """Move all WIP amounts accruded into the CGS account.

        :param datetime.date accounting_date: an optional accounting date to use.
            By default, the date of accounting is the current date.
        """
        self.check_wip_to_cgs_access()
        for project in self:
            project.sudo()._action_wip_to_cgs_single(accounting_date)

        return True

    def check_wip_to_cgs_access(self):
        if not self.env.user.has_group("project_wip.group_wip_to_cgs"):
            raise AccessError(
                _(
                    "Only members of the group 'Transfert WIP to CGS' are allowed to transfer WIP "
                    "entries to CGS."
                )
            )

    def _action_wip_to_cgs_single(self, accounting_date=None):
        """Run the wip to cgs process for a single project."""
        self._check_project_type_has_wip_journal()
        self._check_project_type_has_wip_account()
        self._check_project_type_has_cgs_account()

        unreconciled_wip_lines = self._get_posted_unreconciled_wip_lines()

        for wip_line in unreconciled_wip_lines:
            move = self._create_wip_to_cgs_account_move(wip_line)

            if accounting_date:
                move.date = accounting_date

            wip_reversal_line = move.line_ids.filtered(
                lambda l: l.account_id == self.project_type_id.wip_account_id
            )
            _reconcile_wip_move_lines(wip_line, wip_reversal_line)

            move.post()

    def _create_wip_to_cgs_account_move(self, wip_line):
        """Generate an account move to transfer a WIP amount into CGS.

        :param wip_line: the Work In Progress account move line to transfer into CGS.
        :return: the transfer account move.
        """
        wip_reversal_vals = self._get_common_wip_to_cgs_move_line_vals(wip_line)
        wip_reversal_vals["account_id"] = self.project_type_id.wip_account_id.id
        wip_reversal_vals["debit"] = wip_line.credit if wip_line.credit else 0
        wip_reversal_vals["credit"] = wip_line.debit if wip_line.debit else 0

        cgs_vals = self._get_common_wip_to_cgs_move_line_vals(wip_line)
        cgs_vals["account_id"] = self.project_type_id.cgs_account_id.id
        cgs_vals["debit"] = wip_line.debit if wip_line.debit else 0
        cgs_vals["credit"] = wip_line.credit if wip_line.credit else 0

        return self.env["account.move"].create(
            {
                "company_id": self.company_id.id,
                "journal_id": self.project_type_id.cgs_journal_id.id,
                "no_analytic_lines": True,
                "line_ids": [(0, 0, wip_reversal_vals), (0, 0, cgs_vals)],
            }
        )

    def _check_project_type_has_wip_journal(self):
        """Check that the project type has a wip journal defined.

        :raises: ValidationError if no journal defined.
        """
        if not self.project_type_id.cgs_journal_id:
            raise ValidationError(
                _("The project type {} has no WIP journal defined.").format(
                    self.project_type_id.name
                )
            )

    def _check_project_type_has_wip_account(self):
        """Check that the project type has a wip account defined.

        :raises: ValidationError if no account defined.
        """
        if not self.project_type_id.wip_account_id:
            raise ValidationError(
                _(
                    "The project type {} has no WIP (Work In Progress) account defined."
                ).format(self.project_type_id.name)
            )

    def _check_project_type_has_cgs_account(self):
        """Check that the project type has a cgs account defined.

        :raises: ValidationError if no account defined.
        """
        if not self.project_type_id.cgs_account_id:
            raise ValidationError(
                _(
                    "The project type {} has no CGS (Cost of Goods Sold) account defined."
                ).format(self.project_type_id.name)
            )

    def _get_posted_unreconciled_wip_lines(self):
        """Get WIP lines for this project that are posted and unreconciled.

        :rtype: account.move.line recordset
        """
        return self.env["account.move.line"].search(
            [
                ("analytic_account_id", "=", self.analytic_account_id.id),
                ("account_id", "=", self.project_type_id.wip_account_id.id),
                ("reconciled", "=", False),
                ("move_id.state", "=", "posted"),
            ]
        )

    def _get_common_wip_to_cgs_move_line_vals(self, wip_line):
        """Get the account move line vals common to both the debit and the credit part."""
        return {
            "company_id": self.company_id.id,
            "name": wip_line.name,
            "quantity": wip_line.quantity,
            "product_uom_id": wip_line.product_uom_id.id,
            "product_id": wip_line.product_id.id,
            "partner_id": wip_line.partner_id.id,
            "analytic_account_id": self.analytic_account_id.id,
            "analytic_tag_ids": [(6, 0, wip_line.analytic_tag_ids.ids)],
        }


def _reconcile_wip_move_lines(wip_line, wip_reversal_line):
    """Reconcile a WIP journal item with its reversal.

    :param wip_line: the initial wip account.move.line
    :param wip_reversal_line: the wip reversal account.move.line
    :raises: ValidationError if the lines could not be reconciled.
    """
    unreconciled_line = (wip_line | wip_reversal_line).auto_reconcile_lines()
    if unreconciled_line:
        raise ValidationError(
            _(
                "The WIP entry {wip_line} ({amount}) could not be reconciled when transfering "
                "the amount into Costs of Goods Sold. "
                "You should verify if the WIP entry is partially reconciled."
            ).format(wip_line=wip_line.display_name, amount=wip_line.balance)
        )
