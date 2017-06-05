# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from datetime import datetime
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    """
    The analytic line model must be upgraded so that it can be used
    with the widget.
    """

    _inherit = 'account.analytic.line'

    partner_invoice_id = fields.Many2one(
        'res.partner', 'Partner To Invoice',
        domain=['|', ('customer', '=', True), ('supplier', '=', True)])

    generated_invoice_id = fields.Many2one(
        'account.invoice', 'Generated Invoice')

    show_on_project_invoicing = fields.Boolean(
        'Show On Project Invoicing',
        compute='_compute_show_on_project_invoicing', store=True)

    invoicing_state = fields.Selection([
        ('to_invoice', 'To Invoice'),
        ('draft_invoice', 'Draft Invoice'),
        ('invoiced', 'Invoiced'),
        ('not_invoiceable', 'Not Invoiceable'),
    ], 'Invoicing State', default='to_invoice')

    cost = fields.Monetary(
        'Cost', currency_field='company_currency_id',
        compute='_compute_cost', store=True)
    company_currency_id = fields.Many2one(
        'res.currency', 'Company Currency', related='company_id.currency_id',
        readonly=True)

    sale_price = fields.Monetary(
        'PU (Price List)', compute='_compute_sale_price',
        group_operator=None)
    final_price = fields.Monetary(
        'PU (Final)', currency_field='final_price_currency_id',
        group_operator=None)
    final_price_currency_id = fields.Many2one(
        'res.currency', 'Final Price Currency')
    final_total = fields.Monetary(
        'Total', currency_field='final_price_currency_id',
        compute='_compute_final_total', store=True)

    @api.model
    def create(self, vals):
        line = super(AccountAnalyticLine, self).create(vals)
        if line.project_id:
            line.partner_invoice_id = line.project_id.partner_id
            line._onchange_partner_invoice_id()
        return line

    @api.multi
    def write(self, vals):
        super(AccountAnalyticLine, self).write(vals)
        if vals.get('project_id'):
            project = self.env['project.project'].browse(vals['project_id'])
            self.filtered(lambda l: l.invoicing_state == 'to_invoice').write({
                'partner_invoice_id': project.partner_id.id,
            })
            for line in self:
                if line.invoicing_state == 'to_invoice':
                    line._onchange_partner_invoice_id()
        return True

    @api.depends('amount', 'is_timesheet', 'sheet_id_computed.state')
    def _compute_show_on_project_invoicing(self):
        """
        Only show relevant analytic lines on the widget.

        An analytic line is hidden if it is not an expense
        (null or positive amount) or if it is an unconfirmed
        timesheet line.
        """
        for line in self:
            if(
                line.amount >= 0 or
                line.is_timesheet and line.sheet_id.state != 'done'
            ):
                line.show_on_project_invoicing = False
            else:
                line.show_on_project_invoicing = True

    @api.depends('partner_invoice_id')
    def _compute_sale_price(self):
        for line in self:
            if line.partner_invoice_id and line.product_id:
                if line.unit_amount:
                    price_list = (
                        line.partner_invoice_id.property_product_pricelist)
                    line.sale_price = price_list.get_product_price(
                        line.product_id, line.unit_amount,
                        line.partner_invoice_id,
                        date=datetime.now(), uom_id=line.product_uom_id.id)
                else:
                    line.sale_price = 0

    @api.depends('unit_amount', 'final_price')
    def _compute_final_total(self):
        for line in self:
            line.final_total = line.unit_amount * line.final_price

    @api.depends('amount')
    def _compute_cost(self):
        for line in self:
            line.cost = -line.amount

    @api.onchange('partner_invoice_id')
    def _onchange_partner_invoice_id(self):
        if self.partner_invoice_id:
            price_list = self.partner_invoice_id.property_product_pricelist
            if price_list:
                self.final_price_currency_id = price_list.currency_id
            else:
                self.final_price_currency_id = (
                    self.env.user.company_id.currency_id)

            if self.sale_price:
                self.final_price = self.sale_price
