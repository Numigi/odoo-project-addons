# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.osv.expression import AND


def should_apply_default_template_filter(domain, context):
    template_field_in_domain = any(
        isinstance(el, (list, tuple)) and el[0] == 'is_template'
        for el in domain
    )
    return not (template_field_in_domain or context.get('show_task_templates'))


class ProjectTask(models.Model):

    _inherit = 'project.task'

    is_template = fields.Boolean()

    @api.model
    def _get_values_for_invisible_template_fields(self):
        return {
            'date_deadline': False,
            'email_cc': False,
            'email_from': False,
            'kanban_state': 'normal',
            'partner_id': False,
            'stage_id': False,
            'user_id': False,
        }

    @api.multi
    def write(self, vals):
        if vals.get('is_template'):
            vals = dict(vals, **self._get_values_for_invisible_template_fields())

        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get('is_template'):
            vals = dict(vals, **self._get_values_for_invisible_template_fields())

        return super().create(vals)

    @api.model
    def _search(self, args, *args_, **kwargs):
        """Hide templates from searches by default."""
        if should_apply_default_template_filter(args, self._context):
            args = AND((args or [], [('is_template', '=', False)]))
        return super()._search(args, *args_, **kwargs)
