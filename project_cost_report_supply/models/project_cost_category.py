# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectCostCategory(models.Model):

    _inherit = "project.cost.category"

    section = fields.Selection(selection_add=[("supply", "Shop Supply")])
