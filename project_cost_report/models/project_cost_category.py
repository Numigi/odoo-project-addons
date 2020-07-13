# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectCostCategory(models.Model):

    _name = "project.cost.category"
    _description = "Project Cost Report Group"
    _order = "sequence"

    sequence = fields.Integer()
    name = fields.Char(translate=True, required=True)
    active = fields.Boolean(default=True)

    section = fields.Selection(
        [("products", "Products"), ("time", "Time"), ("outsourcing", "Outsourcing")],
        required=True,
        default="products",
    )

    target_margin = fields.Float()
    target_hourly_rate = fields.Float()
