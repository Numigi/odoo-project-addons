# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    origin_task_id = fields.Many2one(
        'project.task', 'Origin Task',
        ondelete='restrict',
        index=True,
    )


class InvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    task_id = fields.Many2one(
        'project.task', 'Task',
        ondelete='restrict',
        index=True,
    )


class InvoiceTaxLine(models.Model):

    _inherit = 'account.invoice.tax'

    task_id = fields.Many2one(
        'project.task', 'Task',
        ondelete='restrict',
        index=True,
    )


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    task_id = fields.Many2one(
        'project.task', 'Task',
        ondelete='restrict',
        index=True,
    )
