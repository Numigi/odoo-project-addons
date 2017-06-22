# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    origin_id = fields.Reference(
        string='Source Document',
        selection=lambda r: r._selection_origin_id(),
    )

    @api.model
    def _selection_origin_id(self):
        return [(m.model, _(m.name)) for m in self.env['ir.model'].search([])]
