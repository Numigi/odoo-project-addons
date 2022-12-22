# -*- coding: utf-8 -*-
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models

FULL_TEXT_SEARCH_PARAM_KEY = 'postgresql_full_text_search_language'


class IrConfigParameterWithFullTextSearchParamKey(models.Model):
    """Automatically update the gin index on tasks when the full text search language is set."""

    _inherit = 'ir.config_parameter'

    @api.model
    def create(self, vals):
        param = super().create(vals)
        should_update_index = param.key == FULL_TEXT_SEARCH_PARAM_KEY
        if should_update_index:
            self.env['project.task']._setup_content_index()
        return param

    def write(self, vals):
        super().write(vals)
        should_update_index = any(p.key == FULL_TEXT_SEARCH_PARAM_KEY for p in self)
        if should_update_index:
            self.env['project.task']._setup_content_index()
        return True

    def unlink(self):
        should_update_index = any(p.key == FULL_TEXT_SEARCH_PARAM_KEY for p in self)
        super().unlink()
        if should_update_index:
            self.env['project.task']._setup_content_index()
        return True
