# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    @api.onchange("parent_id")
    def _onchange_parent_inherit_sale_object(self):
        if self.parent_id:
            self.sale_order_id = self.parent_id.sale_order_id
            self.sale_line_id = self.parent_id.sale_line_id
