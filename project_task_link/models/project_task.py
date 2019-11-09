# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from urllib.parse import urljoin
from .common import get_html_with_task_links


class Task(models.Model):

    _inherit = 'project.task'

    def get_portal_access_url(self):
        base_url = self.get_base_url()
        return urljoin(base_url, self.access_url)

    @api.multi
    def write(self, vals):
        if vals.get('description'):
            vals['description'] = get_html_with_task_links(self.env, vals['description'])
        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get('description'):
            vals['description'] = get_html_with_task_links(self.env, vals['description'])
        return super().create(vals)
