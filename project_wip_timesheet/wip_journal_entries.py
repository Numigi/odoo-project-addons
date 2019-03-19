# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectType(models.Model):
    """Add the salary account to project types."""

    _inherit = 'project.type'

    salary_account_id = fields.Many2one(
        'account.account',
        'Salary Account',
        company_dependent=True,
    )

    salary_journal_id = fields.Many2one(
        'account.journal',
        'Salary Journal',
        company_dependent=True,
    )

    @api.constrains('salary_account_id', 'salary_journal_id', 'wip_account_id')
    def _check_required_fields_for_salary_entries(self):
        project_types_with_salary_account = self.filtered(lambda t: t.salary_account_id)
        for project_type in project_types_with_salary_account:
            if not project_type.wip_account_id:
                raise ValidationError(_(
                    'If the salary account is filled for a project type, '
                    'the work in progress account must be filled as well.'
                ))

            if not project_type.salary_journal_id:
                raise ValidationError(_(
                    'If the salary account is filled for a project type, '
                    'the salary journal must be filled as well.'
                ))


class TimesheetLine(models.Model):

    _inherit = 'account.analytic.line'

    salary_account_move_id = fields.Many2one(
        'account.move', 'Salary Journal Entry',
        ondelete='restrict',
    )

    def _get_salary_journal(self):
        return self.project_id.project_type_id.salary_journal_id

    def _get_salary_account(self):
        return self.project_id.project_type_id.salary_account_id

    def _get_wip_account(self):
        return self.project_id.project_type_id.wip_account_id

    def _requires_wip_salary_move(self):
        return bool(self._get_salary_account())

    def _get_wip_move_line_vals(self):
        return {
            'account_id': self._get_wip_account().id,
            'name': self.name,
            'debit': -self.amount if self.amount < 0 else 0,
            'credit': self.amount if self.amount > 0 else 0,
            'quantity': self.unit_amount,
            'analytic_account_id': self.project_id.analytic_account_id.id,
        }

    def _get_salary_move_line_vals(self):
        return {
            'account_id': self._get_salary_account().id,
            'name': self.name,
            'debit': self.amount if self.amount > 0 else 0,
            'credit': -self.amount if self.amount < 0 else 0,
            'quantity': self.unit_amount,
        }

    def _get_wip_account_move_vals(self):
        return {
            'company_id': self.company_id.id,
            'journal_id': self._get_salary_journal().id,
            'date': self.date,
            'no_analytic_lines': True,
            'line_ids': [
                (5, 0),
                (0, 0, self._get_wip_move_line_vals()),
                (0, 0, self._get_salary_move_line_vals()),
            ],
        }

    def _create_wip_account_move(self):
        vals = self._get_wip_account_move_vals()
        self.salary_account_move_id = self.env['account.move'].create(vals)
        self.salary_account_move_id.post()

    def _is_wip_account_move_reconciled(self):
        return any(l.full_reconcile_id for l in self.salary_account_move_id.line_ids)

    def _update_wip_account_move(self):
        if self._is_wip_account_move_reconciled():
            raise ValidationError(_(
                'The timesheet line {description} (task: {task}) can not '
                'be updated because the work in progress entry ({move_name}) is already '
                'transfered into the cost of goods sold.'
            ).format(
                description=self.name,
                task=str(self.task_id.id),
                move_name=self.salary_account_move_id.name,
            ))

        self.salary_account_move_id.state = 'draft'
        vals = self._get_wip_account_move_vals()
        self.salary_account_move_id.write(vals)
        self.salary_account_move_id.post()

    def _reverse_salary_account_move_for_updated_timesheet(self):
        if self._is_wip_account_move_reconciled():
            raise ValidationError(_(
                'The timesheet line {description} (task: {task}) can not '
                'be updated because the work in progress entry ({move_name}) would be '
                'reversed. This journal entry was already transfered into '
                'the cost of goods sold.'
            ).format(
                description=self.name,
                task=str(self.task_id.id),
                move_name=self.salary_account_move_id.name,
            ))
        self.salary_account_move_id.reverse_moves()
        self.salary_account_move_id = False

    def _create_update_or_reverse_wip_account_move(self):
        must_update_salary_move = (
            self._requires_wip_salary_move() and self.salary_account_move_id
        )
        must_create_salary_move = (
            self._requires_wip_salary_move() and not self.salary_account_move_id
        )
        must_reverse_salary_move = (
            not self._requires_wip_salary_move() and self.salary_account_move_id
        )

        if must_update_salary_move:
            self._update_wip_account_move()

        elif must_create_salary_move:
            self._create_wip_account_move()

        elif must_reverse_salary_move:
            self._reverse_salary_account_move_for_updated_timesheet()

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if line._requires_wip_salary_move():
            line.sudo()._create_wip_account_move()
        return line

    def _get_salary_move_dependent_fields(self):
        return {
            'name',
            'amount',
            'unit_amount',
            'date',
            'project_id',
        }

    @api.multi
    def write(self, vals):
        super().write(vals)

        fields_to_check = self._get_salary_move_dependent_fields()
        if fields_to_check.intersection(vals):
            for line in self:
                line.sudo()._create_update_or_reverse_wip_account_move()

        return True

    def _reverse_salary_account_move_for_deleted_timesheet(self):
        if self._is_wip_account_move_reconciled():
            raise ValidationError(_(
                'The timesheet line {description} (task: {task}) can not '
                'be deleted because the work in progress entry ({move_name}) is already '
                'transfered into the cost of goods sold.'
            ).format(
                description=self.name,
                task=str(self.task_id.id),
                move_name=self.salary_account_move_id.name,
            ))
        self.salary_account_move_id.reverse_moves()

    @api.multi
    def unlink(self):
        """Reverse the salary account move entry when a timesheet line is deleted."""
        lines_with_moves = self.filtered(lambda l: l.salary_account_move_id)
        for line in lines_with_moves:
            line.sudo()._reverse_salary_account_move_for_deleted_timesheet()
        return super().unlink()
