# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AnalyticLine(models.Model):
    """Prevent an analytic line with a task and analytic account that dont match."""

    _inherit = 'account.analytic.line'

    @api.constrains('origin_task_id', 'account_id')
    def _check_origin_task_and_project_match(self):
        for line in self:
            task_not_matching_project = (
                line.origin_task_id and
                line.origin_task_id.project_id.analytic_account_id != line.account_id
            )
            if task_not_matching_project:
                raise ValidationError(_(
                    'The origin task {task} is set on the analytic line {line}. '
                    'This task does not match the analytic account ({analytic_account}) '
                    'set on the line.'
                ).format(
                    line=line.display_name,
                    task=line.origin_task_id.display_name,
                    analytic_account=line.account_id.display_name
                ))


class InvoiceLine(models.Model):
    """Prevent posting an invoice line with a task and a project that dont match."""

    _inherit = 'account.invoice.line'

    def _check_task_matches_with_project(self):
        task_not_matching_project = (
            self.task_id and
            self.task_id.project_id.analytic_account_id != self.account_analytic_id
        )
        if task_not_matching_project:
            raise ValidationError(_(
                'The task {task} is set on the invoice line {line}. '
                'This task does not match the project ({project}) set on the line.'
            ).format(
                line=self.display_name,
                task=self.task_id.display_name,
                project=self.account_analytic_id.display_name
            ))


class InvoiceTax(models.Model):
    """Prevent posting an invoice tax line with a task and a project that dont match."""

    _inherit = 'account.invoice.tax'

    def _check_task_matches_with_project(self):
        task_not_matching_project = (
            self.task_id and
            self.task_id.project_id.analytic_account_id != self.account_analytic_id
        )
        if task_not_matching_project:
            raise ValidationError(_(
                'The task {task} is set on the tax line {line}. '
                'This task does not match the project ({project}) set on the line.'
            ).format(
                line=self.display_name,
                task=self.task_id.display_name,
                project=self.account_analytic_id.display_name
            ))


class Invoice(models.Model):
    """Prevent posting an invoice with a task and a project that dont match."""

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        for line in self.mapped('invoice_line_ids'):
            line._check_task_matches_with_project()

        for tax in self.mapped('tax_line_ids'):
            tax._check_task_matches_with_project()

        return super().action_invoice_open()


class AccountMoveLine(models.Model):
    """Prevent posting an journal item with a task and a project that dont match."""

    _inherit = 'account.move.line'

    def _check_task_matches_with_project(self):
        task_not_matching_project = (
            self.task_id and
            self.task_id.project_id.analytic_account_id != self.analytic_account_id
        )
        if task_not_matching_project:
            raise ValidationError(_(
                'The task {task} is set on the journal item {line}. '
                'This task does not match the project ({project}) set on the line.'
            ).format(
                line=self.display_name,
                task=self.task_id.display_name,
                project=self.analytic_account_id.display_name
            ))


class AccountMove(models.Model):
    """Prevent posting a journal entry with a task and a project that dont match."""

    _inherit = 'account.move'

    @api.multi
    def post(self):
        for line in self.mapped('line_ids'):
            line._check_task_matches_with_project()

        return super().post()


class Task(models.Model):
    """Prevent moving the task when used on journal entries.

    When the task is used on a journal entry, the task must not be
    moved to another project.

    A constraint is also checked on open invoices.
    This allows to return a more precise error message to the user.
    """

    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        if 'project_id' in vals:
            tasks_with_changed_project = self.filtered(
                lambda t: t.project_id.id != vals['project_id'])

            for task in tasks_with_changed_project:
                task._check_no_related_open_invoice()
                task._check_no_related_journal_entry()

        return super().write(vals)

    @api.multi
    def _check_no_related_open_invoice(self):
        invoice_lines = self.env['account.invoice.line'].sudo().search([
            ('task_id', 'in', self.ids),
            ('invoice_id.state', 'in', ('open', 'paid')),
        ])
        if invoice_lines:
            task = invoice_lines[0].task_id
            invoice = invoice_lines[0].invoice_id
            raise ValidationError(_(
                'The task {task} can not be moved to another project '
                'because it is already bound to a validated invoice ({invoice}).'
            ).format(task=task.display_name, invoice=invoice.display_name))

    @api.multi
    def _check_no_related_journal_entry(self):
        move_lines = self.env['account.move.line'].sudo().search([
            ('task_id', 'in', self.ids),
            ('move_id.state', '=', 'posted'),
        ])
        if move_lines:
            task = move_lines[0].task_id
            move = move_lines[0].move_id
            raise ValidationError(_(
                'The task {task} can not be moved to another project '
                'because it is already bound to a posted journal entry ({move}).'
            ).format(task=task.display_name, move=move.display_name))
