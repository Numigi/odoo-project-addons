# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
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
        [
            ("products", "Products"),
            ("time", "Time"),
            ("outsourcing", "Outsourcing"),
        ],
        required=True,
        default="products",
    )

    target_type = fields.Selection(
        [
            ("percent", "Percentage"),
            ("hourly_rate", "Hourly Rate"),
        ],
        required=True,
        default="percent",
    )

    target_margin = fields.Float()
    target_hourly_rate = fields.Float()

    @api.onchange("section")
    def _onchange_section_set_target_type(self):
        if self.section != "time":
            self.target_type = "percent"
