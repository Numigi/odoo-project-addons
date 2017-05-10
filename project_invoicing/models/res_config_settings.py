# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import fields, models


class ProjectConfigSettings(models.TransientModel):

    _inherit = 'project.config.settings'

    invoicing_product_global_id = fields.Many2one(
        'product.product', 'Default Product on Invoices (Global Amount)')

    def set_invoicing_product_global_id(self):
        self.env['ir.values'].set_default(
            'project_invoicing', 'invoicing_product_global_id',
            self.invoicing_product_global_id.id)

    def get_default_invoicing_product_global_id(self, fields):
        return {
            'invoicing_product_global_id': self.env['ir.values'].get_default(
                'project_invoicing', 'invoicing_product_global_id')
        }
