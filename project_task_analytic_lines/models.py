# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    origin_task_id = fields.Many2one(
        'project.task', 'Origin Task',
        ondelete='restrict',
        index=True,
    )

    @api.onchange('account_id')
    def _onchange_analytic_account_empty_task(self):
        if self.account_id != self.origin_task_id.project_id.analytic_account_id:
            self.origin_task_id = False


class InvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    task_id = fields.Many2one(
        'project.task', 'Task',
        ondelete='restrict',
        index=True,
    )

    @api.onchange('account_analytic_id')
    def _onchange_analytic_account_empty_task(self):
        if self.account_analytic_id != self.task_id.project_id.analytic_account_id:
            self.task_id = False


class InvoiceTaxLine(models.Model):

    _inherit = 'account.invoice.tax'

    task_id = fields.Many2one(
        'project.task', 'Task',
        ondelete='restrict',
        index=True,
    )

    @api.onchange('account_analytic_id')
    def _onchange_analytic_account_empty_task(self):
        if self.account_analytic_id != self.task_id.project_id.analytic_account_id:
            self.task_id = False


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    task_id = fields.Many2one(
        'project.task', 'Task',
        ondelete='restrict',
        index=True,
    )

    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_empty_task(self):
        if self.analytic_account_id != self.task_id.project_id.analytic_account_id:
            self.task_id = False
