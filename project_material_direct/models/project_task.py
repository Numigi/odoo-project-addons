# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


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

    direct_consumption_total = fields.Monetary(
        "Direct Consumption Total",
        compute="_compute_direct_consumption_total",
        store=True,
        track_visibility="onchange",
    )

    @api.depends("direct_material_line_ids.consumed_subtotal")
    def _compute_direct_consumption_total(self):
        """
        Total of all material lines direct consumption.
        """
        for record in self:
            record.direct_consumption_total = sum(
                record.direct_material_line_ids.mapped("consumed_subtotal")
            )

    @api.depends("consumption_total", "direct_consumption_total")
    def _compute_consumed_total(self):
        """
        Override of _compute_consumed_total To add direct consumption total.
        """
        for record in self:
            record.consumed_total = (
                record.consumption_total + record.direct_consumption_total
            )
