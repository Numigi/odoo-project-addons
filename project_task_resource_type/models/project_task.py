# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    resource_id = fields.Many2one('project.resource')
