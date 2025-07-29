# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectWithChatter(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'mail.activity.mixin']

    date = fields.Date(tracking=True)
    date_start = fields.Date(tracking=True)
