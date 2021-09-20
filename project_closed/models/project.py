# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):

    _inherit = "project.project"

    closed = fields.Boolean(related="stage_id.closed", store=True)
