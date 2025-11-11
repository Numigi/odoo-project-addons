# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectStage(models.Model):

    _inherit = "project.stage"

    closed = fields.Boolean()
