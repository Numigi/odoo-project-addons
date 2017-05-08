# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    task_id = fields.Many2one('project.task', 'Task', ondelete='restrict')

    @api.constrains('task_id')
    def _check_task_project(self):
        for line in self:
            invoice_projects = line.account_analytic_id.project_ids
            task_project = line.task_id.project_id

            if (
                task_project and invoice_projects and
                task_project not in invoice_projects
            ):
                raise UserError(_(
                    'The invoice line (%(line)s) has a task '
                    '(%(task)s) and the invoice has a project '
                    '(%(invoice_project)s), but the task is bound to '
                    'the project (%(task_project)s).') % {
                        'line': line.name,
                        'task': line.task_id.name,
                        'invoice_project': invoice_projects[0].name,
                        'task_project': task_project.name,
                })
