# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_additional = fields.Boolean(
        string="Additional", default=lambda self: self._default_is_additional()
    )

    @api.model
    def _default_is_additional(self):
        return bool(self.env.context.get('default_parent_id'))

    @api.onchange('parent_id')
    def _onchange_parent_id_to_additional(self):
        self.is_additional = bool(self.parent_id)
