# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    """Generate WIP journal entries for consumption moves."""

    _inherit = 'stock.move'

    def _is_consumption(self):
        return self.picking_code == 'consumption'

    def _is_consumption_return(self):
        return self.picking_code == 'consumption_return'

    def _check_project_has_wip_account(self):
        project = self.project_id
        if not project.project_type_id:
            raise ValidationError(_(
                'The transfer {picking} can not be processed because '
                'the project {project} has no project type.'
            ).format(
                picking=self.picking_id.name,
                project=project.display_name,
            ))

        if not project.project_type_id.wip_account_id:
            raise ValidationError(_(
                'The transfer {picking} can not be processed because '
                'the project type {project_type} has no WIP account.'
            ).format(
                picking=self.picking_id.name,
                project_type=project.project_type_id.display_name,
            ))

    def _get_wip_account(self):
        return self.project_id.project_type_id.wip_account_id

    def _get_project_analytic_account(self):
        return self.project_id.analytic_account_id

    def _generate_consumption_account_move(self):
        self._check_project_has_wip_account()
        wip_account = self._get_wip_account()
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        self._create_account_move_line(
            debit_account_id=wip_account.id, credit_account_id=acc_valuation, journal_id=journal_id)

    def _generate_consumption_return_account_move(self):
        self._check_project_has_wip_account()
        wip_account = self._get_wip_account()
        journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
        self._create_account_move_line(
            debit_account_id=acc_valuation, credit_account_id=wip_account.id, journal_id=journal_id)

    def _account_entry_move(self):
        self.ensure_one()
        if self._is_consumption():
            self._generate_consumption_account_move()
        elif self._is_consumption_return():
            self._generate_consumption_return_account_move()
        else:
            super()._account_entry_move()

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
        """Add the analytic to WIP account move lines."""
        move_line_vals = super()._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)

        if self._is_consumption() or self._is_consumption_return():
            wip_account = self._get_wip_account()
            analytic_account = self._get_project_analytic_account()
            lines_with_wip_account = (
                line for line in move_line_vals
                if line[2]['account_id'] == wip_account.id
            )
            for line in lines_with_wip_account:
                line[2]['analytic_account_id'] = analytic_account.id

        return move_line_vals


class TaskMaterialLine(models.Model):
    """Prevent adding material the project is not properly set for accounting."""

    _inherit = 'project.task.material'

    def _check_project_has_wip_account(self):
        project = self.task_id.project_id
        if not project.project_type_id:
            raise ValidationError(_(
                'Material can not be added to the task because '
                'the project {} has no project type.'
            ).format(project.display_name))

        if not project.project_type_id.wip_account_id:
            raise ValidationError(_(
                'Material can not be added to the task because '
                'the project type {} has no WIP account.'
            ).format(project.project_type_id.display_name))

    def _generate_procurements(self):
        self._check_project_has_wip_account()
        return super()._generate_procurements()
