# Copyright 2025 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    task_id = fields.Many2one(
        "project.task", string="Task", index=True, copy=False
    )
    material_line_id = fields.Many2one(
        "project.task.material", string="Material Line", index=True, copy=False
    )

    @api.model
    def _prepare_purchase_order_line_from_procurement(
        self, product_id, product_qty, product_uom, company_id, values, po
    ):
        vals = super()._prepare_purchase_order_line_from_procurement(
            product_id, product_qty, product_uom, company_id, values, po
        )
        if "task_id" in values and values["task_id"]:
            vals["task_id"] = values["task_id"]
        vals["material_line_id"] = values["move_dest_ids"].material_line_id.id
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(PurchaseOrderLine, self).create(vals_list)
        for line in lines:
            if line.material_line_id:
                line.material_line_id.purchase_line_id = line.id
        return lines

    def write(self, values):
        for line in self.filtered(lambda pl: not pl.display_type):
            if values.get("material_line_id"):
                material_line_id = self.env["project.task.material"].browse(
                    values.get("material_line_id")
                )
                material_line_id.purchase_line_id = line.id
        return super(PurchaseOrderLine, self).write(values)
