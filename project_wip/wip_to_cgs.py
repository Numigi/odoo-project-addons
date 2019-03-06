# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectType(models.Model):

    _inherit = 'project.type'

    cgs_journal_id = fields.Many2one(
        'account.journal', 'WIP To CGS Journal',
        help="Accounting journal used when transfering WIP journal items into CGS."
    )
    wip_account_id = fields.Many2one(
        'account.account', 'WIP Account',
        help="Account used to cumulate Work In Progress for this project type."
    )
    cgs_account_id = fields.Many2one(
        'account.account', 'CGS Account',
        help="Account used to cumulate Costs of Goods Sold for this project type."
    )

    @api.constrains('wip_account_id')
    def _check_wip_account_allows_reconcile(self):
        """Check that the wip account on project type allows reconciliation."""
        project_types_with_wip_accounts = self.filtered(lambda t: t.wip_account_id)
        for project_type in project_types_with_wip_accounts:
            if not project_type.wip_account_id.reconcile:
                raise ValidationError(
                    _('The selected WIP account ({}) must allow reconciliation.')
                    .format(project_type.wip_account_id.display_name)
                )


class Project(models.Model):

    _inherit = 'project.project'

    def _check_project_type_has_wip_journal(self):
        """Check that the project type has a wip journal defined.

        :raises: ValidationError if no journal defined.
        """
        if not self.project_type_id.cgs_journal_id:
            raise ValidationError(
                _('The project type {} has no WIP journal defined.')
                .format(self.project_type_id.name)
            )

    def _check_project_type_has_wip_account(self):
        """Check that the project type has a wip account defined.

        :raises: ValidationError if no account defined.
        """
        if not self.project_type_id.wip_account_id:
            raise ValidationError(
                _('The project type {} has no WIP (Work In Progress) account defined.')
                .format(self.project_type_id.name)
            )

    def _check_project_type_has_cgs_account(self):
        """Check that the project type has a cgs account defined.

        :raises: ValidationError if no account defined.
        """
        if not self.project_type_id.cgs_account_id:
            raise ValidationError(
                _('The project type {} has no CGS (Cost of Goods Sold) account defined.')
                .format(self.project_type_id.name)
            )

    def _get_posted_unreconciled_wip_lines(self):
        """Get WIP lines for this project that are posted and unreconciled.

        :rtype: account.move.line recordset
        """
        return self.env['account.move.line'].search([
            ('analytic_account_id', '=', self.analytic_account_id.id),
            ('account_id', '=', self.project_type_id.wip_account_id.id),
            ('reconciled', '=', False),
            ('move_id.state', '=', 'posted'),
        ])

    def _get_common_wip_to_cgs_move_line_vals(self, wip_line):
        """Get the account move line vals common to both the debit and the credit part."""
        return {
            'name': wip_line.name,
            'quantity': wip_line.quantity,
            'product_uom_id': wip_line.product_uom_id.id,
            'product_id': wip_line.product_id.id,
            'partner_id': wip_line.partner_id.id,
            'analytic_account_id': self.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, wip_line.analytic_tag_ids.ids)],
        }

    def _create_wip_to_cgs_account_move(self, wip_line):
        """Generate an account move to transfer a WIP amount into CGS.

        :param wip_line: the Work In Progress account move line to transfer into CGS.
        :return: the transfer account move.
        """
        wip_reversal_vals = self._get_common_wip_to_cgs_move_line_vals(wip_line)
        wip_reversal_vals['account_id'] = self.project_type_id.wip_account_id.id
        wip_reversal_vals['debit'] = wip_line.credit if wip_line.credit else 0
        wip_reversal_vals['credit'] = wip_line.debit if wip_line.debit else 0

        cgs_vals = self._get_common_wip_to_cgs_move_line_vals(wip_line)
        cgs_vals['account_id'] = self.project_type_id.cgs_account_id.id
        cgs_vals['debit'] = wip_line.debit if wip_line.debit else 0
        cgs_vals['credit'] = wip_line.credit if wip_line.credit else 0

        return self.env['account.move'].create({
            'journal_id': self.project_type_id.cgs_journal_id.id,
            'no_analytic_lines': True,
            'line_ids': [
                (0, 0, wip_reversal_vals),
                (0, 0, cgs_vals),
            ]
        })

    def _reconcile_wip_move_lines(self, wip_line, wip_reversal_line):
        """Reconcile a WIP journal item with its reversal.

        :param wip_line: the initial wip account.move.line
        :param wip_reversal_line: the wip reversal account.move.line
        :raises: ValidationError if the lines could not be reconciled.
        """
        unreconciled_line = (wip_line | wip_reversal_line).auto_reconcile_lines()
        if unreconciled_line:
            raise ValidationError(
                _('The WIP entry {wip_line} ({amount}) could not be reconciled when transfering '
                  'the amount into Costs of Goods Sold. '
                  'You should verify if the WIP entry is partially reconciled.')
                .format(
                    wip_line=wip_line.display_name,
                    amount=wip_line.balance,
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
                lambda l: l.account_id == self.project_type_id.wip_account_id)
            self._reconcile_wip_move_lines(wip_line, wip_reversal_line)

            move.post()

    @api.multi
    def action_wip_to_cgs(self, accounting_date=None):
        """Move all WIP amounts accruded into the CGS account.

        :param datetime.date accounting_date: an optional accounting date to use.
            By default, the date of accounting is the current date.
        """
        for project in self:
            project._action_wip_to_cgs_single(accounting_date)

        return True


class ProjectWipTransferWizard(models.TransientModel):
    """Wizard that allows to define a custom date to post the WIP transfer move."""

    _name = 'project.wip.transfer'
    _description = 'Project WIP To CGS Wizard'

    project_id = fields.Many2one('project.project', 'Project')
    cgs_journal_id = fields.Many2one(related='project_id.project_type_id.cgs_journal_id')
    wip_account_id = fields.Many2one(related='project_id.project_type_id.wip_account_id')
    cgs_account_id = fields.Many2one(related='project_id.project_type_id.cgs_account_id')
    accounting_date = fields.Date(
        default=fields.Date.context_today,
        help="The selected date will be used for posting the journal entries "
        "when transfering amounts from WIP to CGS."
    )
    costs_to_transfer = fields.Monetary()
    currency_id = fields.Many2one(
        'res.currency', 'Currency', related='project_id.company_id.currency_id'
    )

    @api.onchange('project_id')
    def _onchange_project_compute_costs_to_transfer(self):
        has_wip_account = bool(self.wip_account_id)
        if has_wip_account:
            self.costs_to_transfer = sum(
                line.balance
                for line in self.project_id._get_posted_unreconciled_wip_lines()
            )

    def validate(self):
        return self.project_id.action_wip_to_cgs(self.accounting_date)
