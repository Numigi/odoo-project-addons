# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, Warning as UserError


class ProjectProject(models.Model):

    _inherit = 'project.project'

    # The field task_ids only displays tasks that are not in a folded stage
    all_task_ids = fields.One2many(
        'project.task', 'project_id', string='All Tasks')

    @api.multi
    def generate_invoices(self, data):
        self.ensure_one()
        invoices = self._create_invoices(data)
        action = self.env.ref('account.action_invoice_tree1')
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
            'domain': [('id', 'in', invoices.ids)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

    @api.multi
    def _create_invoices(self, data):
        self.ensure_one()
        self = self.with_context(
            force_company=self.company_id.id,
            company_id=self.company_id.id)

        inv_lines = defaultdict(list)
        analytic_line_ids = defaultdict(list)

        for task_id, values in data['tasks'].items():
            task = self.env['project.task'].browse(int(task_id))
            assert task.project_id == self

            if not values['lines']:
                raise UserError(_(
                    "You did not select any analytic line for the "
                    "task %(task)s."
                ) % {'task': task.name})

            task.prepare_analytic_lines(values['lines'])

            if values['mode'] == 'real':
                for line in values['lines']:
                    if(
                        not line['final_price_currency_id'] or
                        not line['partner_invoice_id']
                    ):
                        raise UserError(_(
                            "You must select a partner to invoice and "
                            "a currency for each line selected for invoicing "
                            "in mode real."
                        ))

                    currency_id = int(line['final_price_currency_id'][0])
                    partner_id = int(line['partner_invoice_id'][0])

                    key = (partner_id, currency_id)
                    inv_lines[key].append(
                        self._get_invoice_line_vals_real(line))
                    analytic_line_ids[key].append(int(line['id']))

            else:
                currency_id = int(values['currency_id'])
                partner_id = int(values['partner_id'])
                key = (partner_id, currency_id)
                inv_lines[key].extend(
                    self._get_invoice_line_vals_lump_sum(values))
                analytic_line_ids[key].extend([
                    int(l['id']) for l in values['lines']
                ])

        invoices = self.env['account.invoice']
        inv_obj = self.env['account.invoice'].with_context(type='out_invoice')

        for (partner_id, currency_id), lines in inv_lines.items():
            vals = self._get_invoice_vals(partner_id, currency_id)
            vals['invoice_line_ids'] = [(0, 0, l) for l in lines]
            vals['source_analytic_line_ids'] = [
                (6, 0, analytic_line_ids[(partner_id, currency_id)])
            ]
            invoices |= inv_obj.create(vals)

        return invoices

    @api.multi
    def _get_invoice_vals(self, partner_id, currency_id):
        self.ensure_one()
        partner = self.env['res.partner'].browse(partner_id)

        if not partner.property_account_receivable_id:
            raise ValidationError(_(
                'The receivable account for the partner %(partner)s '
                'is not set. It is therefore not possible to generate '
                'an invoice for this partner.'))

        vals = {
            'partner_id': partner_id,
            'currency_id': currency_id,
            'company_id': self.company_id.id,
            'account_id': partner.property_account_receivable_id.id,
            'fiscal_position_id': partner.property_account_position_id.id,
            'is_project_invoice': True,
        }

        if currency_id == self.company_id.currency_id.id:
            journal = self.env['account.journal'].search([
                '|',
                ('currency_id', '=', False),
                ('currency_id', '=', currency_id),
                ('company_id', '=', self.company_id.id),
                ('type', '=', 'sale'),
            ], limit=1)
        else:
            journal = self.env['account.journal'].search([
                ('currency_id', '=', currency_id),
                ('company_id', '=', self.company_id.id),
                ('type', '=', 'sale'),
            ], limit=1)

        if not journal:
            raise UserError(_(
                'There is no available sale journal for the currency %s.'
            ) % self.env['res.currency'].browse(currency_id).name)

        vals['journal_id'] = journal.id

        return vals

    @api.multi
    def _get_default_income_account(self):
        self.ensure_one()
        property_obj = self.env['ir.property']

        account = property_obj.get(
            'property_account_income_id', 'product.template')

        if not account:
            account = property_obj.get(
                'property_account_income_categ_id', 'product.category')

        if not account:
            raise ValidationError(_(
                'The invoice could not be generated from the '
                'project %(project)s. The default income account '
                'is not set on the company %(company)s.'
            ) % {
                'project': self.name,
                'company': self.company_id.name,
            })

        return account

    @api.multi
    def _get_income_account(self, partner, product):
        fiscal_pos = partner.property_account_position_id
        account = self.env['account.invoice.line'].get_invoice_line_account(
            'out_invoice', product, fiscal_pos, self.company_id)
        return account or self._get_default_income_account()

    @api.multi
    def _get_invoice_line_vals_real(self, line_values):
        self.ensure_one()
        line = self.env['account.analytic.line'].browse(int(line_values['id']))
        partner = line.partner_invoice_id
        product = line.product_id

        return {
            'name': line.name,
            'account_id': self._get_income_account(partner, product).id,
            'product_id': product.id,
            'quantity': line.unit_amount,
            'price_unit': line.final_price,
            'task_id': line.task_id.id,
            'account_analytic_id': line.account_id.id,
        }

    @api.multi
    def _get_invoice_line_vals_lump_sum(self, values):
        self.ensure_one()
        product = self.env['product.product'].browse(
            int(values['global_amount_product_id']))
        partner = self.env['res.partner'].browse(int(values['partner_id']))

        return [{
            'account_id': self._get_income_account(partner, product).id,
            'name': product.description_sale or '/',
            'quantity': 1,
            'price_unit': float(values['global_amount']),
            'task_id': int(values['id']),
            'account_analytic_id': self.analytic_account_id.id,
            'product_id': product.id,
        }]
