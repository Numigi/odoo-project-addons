# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import fields, models


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    task_id = fields.Many2one('project.task', 'Task', ondelete='restrict')
