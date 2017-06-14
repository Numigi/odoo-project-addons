# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):

    _inherit = 'project.task'

    company_currency_id = fields.Many2one(
        'res.currency', related='company_id.currency_id', readonly=True)
    invoiced_amount = fields.Monetary(
        'Invoiced Amount', currency_field='company_currency_id',
        compute='_compute_invoiced_amount')
    invoice_line_ids = fields.One2many(
        'account.invoice.line', 'task_id', 'Invoice Lines')
    project_partner = fields.Many2one(
        'res.partner', 'Project Partner', related='project_id.partner_id')

    @api.multi
    def _compute_invoiced_amount(self):
        for task in self:
            total = 0
            to_currency = task.company_currency_id

            for line in task.invoice_line_ids:
                if (
                    line.invoice_id.type in ('out_invoice', 'out_refund') and
                    line.invoice_id.state != 'cancel'
                ):
                    invoice = line.invoice_id
                    total += invoice.currency_id.with_context(
                        date=invoice.date_invoice).compute(
                            line.price_subtotal, to_currency)
            task.invoiced_amount = to_currency.round(total)

    @api.multi
    def prepare_analytic_lines(self, lines):
        self.ensure_one()

        line_obj = self.env['account.analytic.line']
        for values in lines:
            record = line_obj.browse(int(values['id']))

            if record.invoicing_state != 'to_invoice':
                raise ValidationError(_(
                    'The analytic line %(line)s is already '
                    'invoiced (%(invoice)s). It may not be invoiced twice.'
                ) % {
                    'line': record.name,
                    'invoice': record.generated_invoice_id.name,
                })

            assert record.task_id == self
            vals = {'invoicing_state': 'draft_invoice'}

            if 'partner_invoice_id' in values:
                partner_id = values['partner_invoice_id']
                partner_id = int(partner_id[0]) if partner_id else False
                if partner_id != record.partner_invoice_id.id:
                    vals['partner_invoice_id'] = partner_id

            if 'final_price_currency_id' in values:
                cur_id = values['final_price_currency_id']
                cur_id = int(cur_id[0]) if cur_id else False
                if cur_id != record.final_price_currency_id.id:
                    vals['final_price_currency_id'] = cur_id

            if 'final_price' in values:
                price = float(values['final_price'])
                if price != record.final_price:
                    vals['final_price'] = price

            if vals:
                record.write(vals)

    @api.multi
    def get_invoice_list_action(self):
        self.ensure_one()
        action = self.env.ref('account.action_invoice_tree1')

        invoice_ids = list(set([
            l.invoice_id.id for l in self.invoice_line_ids
            if l.invoice_id.type in ('out_invoice', 'out_refund')]))

        return {
            'name': action.name,
            'view_type': 'form',
            'view_mode': 'list,form',
            'res_model': 'account.invoice',
            'views': [
                (self.env.ref('account.invoice_tree').id, 'list'),
                (self.env.ref('account.invoice_form').id, 'form'),
            ],
            'search_view_id': action.search_view_id.id,
            'context': action.context,
            'domain': [('id', 'in', invoice_ids)],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
