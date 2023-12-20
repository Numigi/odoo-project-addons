# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):
    """Add warehouse to project."""

    _inherit = "project.project"

    def _get_default_warehouse(self):
        company = self.env.user.company_id
        warehouse = self.env["stock.warehouse"].search(
            [("company_id", "=", company.id)], limit=1
        )
        return warehouse

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        "Warehouse",
        ondelete="restrict",
        default=_get_default_warehouse,
    )

    material_line_ids = fields.One2many(
        "project.task.material", "project_id", "Material"
    )
