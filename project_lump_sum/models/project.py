# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    lump_sum = fields.Boolean(related="type_id.lump_sum", store=True)
