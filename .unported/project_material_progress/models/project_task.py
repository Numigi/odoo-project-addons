# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    has_material = fields.Boolean(
        store=True, compute="_compute_has_material", compute_sudo=True
    )
    material_progress = fields.Float(
        store=True, compute="_compute_material_progress", compute_sudo=True
    )

    @api.depends("material_line_ids")
    def _compute_has_material(self):
        for task in self:
            task.has_material = bool(task.material_line_ids)

    @api.depends(
        "material_line_ids.consumed_qty",
        "material_line_ids.prepared_qty",
        "material_line_ids.initial_qty",
    )
    def _compute_material_progress(self):
        for task in self:
            task.material_progress = task._get_material_progress()

    def _get_material_progress(self):
        units = self.env.ref("uom.product_uom_unit")
        units_category = units.category_id
        material_lines = self.material_line_ids.filtered(
            lambda l: l.product_uom_id.category_id == units_category
        )
        prepared = sum(
            l.product_uom_id._compute_quantity(l.prepared_qty, units)
            for l in material_lines
        )
        consumed = sum(
            l.product_uom_id._compute_quantity(l.consumed_qty, units)
            for l in material_lines
        )
        initial = sum(
            l.product_uom_id._compute_quantity(l.initial_qty, units)
            for l in material_lines
        )
        return max(prepared, consumed) * 100 / initial if initial else 0
