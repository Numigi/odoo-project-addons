# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectResource(models.Model):
    _name = 'project.resource'
    _inherit = ['mail.thread']
    _description = 'Project Resource'

    name = fields.Char(string='Name')
