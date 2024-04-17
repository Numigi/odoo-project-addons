# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class Task(models.Model):

    _inherit = "project.task"

    material_line_ids = fields.One2many(domain=[("is_direct_consumption", "=", False)])

    direct_material_line_ids = fields.One2many(
        "project.task.material",
        "task_id",
        "Material (Direct Consumption)",
        readonly=True,
        domain=[("is_direct_consumption", "=", True)],
    )

    total_direct_consumption = fields.Float(
        "Total Direct Consumption",
        compute="_compute_total_direct_consumption",
    )

    total_consumed = fields.Float(
        "Total Consumed",
        compute="_compute_total_consumed",
    )

    @api.depends("total_direct_consumption", "total_consumption")
    def _compute_total_consumed(self):
        """
        Total of all consumptions, direct or not.
        """
        for record in self:
            record.total_consumed = (
                record.total_direct_consumption + record.total_consumption
            )

    @api.depends("direct_material_line_ids.direct_consumption_subtotal")
    def _compute_total_direct_consumption(self):
        """
        Total of all material lines direct consumption.
        """
        for record in self:
            record.total_direct_consumption = sum(
                record.direct_material_line_ids.mapped("direct_consumption_subtotal")
            )
