# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_task_autocreate_ids = fields.One2many(
        string='Follow-up Preferences',
        comodel_name='partner.task.autocreate',
        inverse_name='partner_id',
    )
