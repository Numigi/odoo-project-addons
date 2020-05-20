# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    project_cost_category_id = fields.Many2one(
        "project.cost.category", "Cost Report Category", ondelete="restrict"
    )

    @api.onchange("parent_id")
    def _propagate_cost_category_from_parent(self):
        self.project_cost_category_id = self.parent_id.project_cost_category_id
