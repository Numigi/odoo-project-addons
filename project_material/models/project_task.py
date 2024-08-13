# Copyright 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date
from odoo import api, fields, models


class TaskWithMaterialLines(models.Model):
    """Add material consumption to tasks."""

    _inherit = "project.task"

    material_line_ids = fields.One2many("project.task.material", "task_id", "Material")

    procurement_group_id = fields.Many2one(
        "procurement.group", "Procurement Group", copy=False
    )

    consumption_picking_count = fields.Integer(
        compute="_compute_consumption_pickings", readonly=False
    )
    consumption_picking_ids = fields.One2many(
        "stock.picking",
        string="Consumption Pickings",
        compute="_compute_consumption_pickings",
    )

    preparation_picking_count = fields.Integer(
        compute="_compute_preparation_pickings", readonly=False
    )
    preparation_picking_ids = fields.One2many(
        "stock.picking",
        string="Preparation Pickings",
        compute="_compute_preparation_pickings",
    )
    preparation_return_picking_count = fields.Integer(
        compute="_compute_preparation_pickings", readonly=False
    )
    preparation_return_picking_ids = fields.One2many(
        "stock.picking",
        string="Preparation Return Pickings",
        compute="_compute_preparation_pickings",
    )

    show_material_prepared_qty = fields.Boolean(
        compute="_compute_show_material_prepared_qty"
    )

    procurement_disabled = fields.Boolean()

    def _compute_preparation_pickings(self):
        tasks_with_procurement_group = self.filtered(lambda t: t.procurement_group_id)
        for task in tasks_with_procurement_group:
            pickings = self.env["stock.picking"].search(
                [
                    ("group_id", "=", task.procurement_group_id.id),
                    ("picking_type_code", "=", "internal"),
                ]
            )
            prep_picking = pickings.filtered(
                lambda p: not _is_preparation_return_picking(p)
            )
            return_picking = pickings.filtered(
                lambda p: _is_preparation_return_picking(p)
            )
            task.preparation_picking_ids = prep_picking
            task.preparation_picking_count = len(prep_picking)
            task.preparation_return_picking_ids = return_picking
            task.preparation_return_picking_count = len(return_picking)

    def _compute_consumption_pickings(self):
        tasks_with_procurement_group = self.filtered(lambda t: t.procurement_group_id)
        for task in tasks_with_procurement_group:
            pickings = self.env["stock.picking"].search(
                [
                    ("group_id", "=", task.procurement_group_id.id),
                    ("picking_type_code", "in", ("consumption", "consumption_return")),
                ]
            )
            task.consumption_picking_ids = pickings
            task.consumption_picking_count = len(pickings)

    def _compute_show_material_prepared_qty(self):
        for task in self:
            task.show_material_prepared_qty = (
                task.project_id.warehouse_id.consu_steps == "two_steps"
            )

    def write(self, vals):
        super().write(vals)
        for task in self:
            if "procurement_disabled" in vals or "material_line_ids" in vals:
                procurement_disabled = (
                    vals.get("procurement_disabled") or self.procurement_disabled
                )
                if procurement_disabled:
                    task._cancel_procurements()
                else:
                    task._run_procurements()
            if "date_planned" in vals:
                task._propagate_planned_date_to_stock_moves()
        return True

    def copy(self, vals=None):
        task = super().copy(vals)

        if self.material_line_ids:
            task.procurement_disabled = True
            task._copy_material_lines_from(self)

        return task

    @api.onchange("project_id")
    def _onchange_project_enable_procurements(self):
        if self.project_id:
            self.procurement_disabled = False

    def _copy_material_lines_from(self, task):
        if not self.date_planned:
            self.date_planned = date(2099, 1, 1)

        for line in task.material_line_ids:
            line.copy({"task_id": self.id})

    def _run_procurements(self):
        for line in self.mapped("material_line_ids"):
            line._run_procurements()

    def _cancel_procurements(self):
        for line in self.mapped("material_line_ids"):
            line._cancel_procurements()

    def _propagate_planned_date_to_stock_moves(self):
        for line in self.mapped("material_line_ids"):
            line._propagate_planned_date_to_stock_moves()

    def _get_procurement_group(self):
        if not self.procurement_group_id:
            self.procurement_group_id = self.env["procurement.group"].create(
                {"name": self._get_reference_for_procurements(), "task_id": self.id}
            )
        return self.procurement_group_id

    def _get_reference_for_procurements(self):
        return "TA#{}".format(str(self.id))

    def open_consumption_picking_view_from_task(self):
        """Open the view of consumption pickings related to the task.

        If there are multiple pickings, open the list view.
        Otherwise, open the form view.

        This method is inspired by the method action_view_delivery
        of sale.order. This method can be found at

        odoo/addons/sale_stock/models/sale_order.py
        """
        return self._open_stock_pickings_view_from_task(self.consumption_picking_ids)

    def open_preparation_picking_view_from_task(self):
        return self._open_stock_pickings_view_from_task(self.preparation_picking_ids)

    def open_preparation_return_picking_view_from_task(self):
        return self._open_stock_pickings_view_from_task(
            self.preparation_return_picking_ids
        )

    def _open_stock_pickings_view_from_task(self, pickings):
        """Open the view of pickings related to the task.

        The view is constrained to the given set of pickings.

        This method is intended to be inherited to show the list/form view
        of different types of picking related to the task.
        """
        action = self.env.ref("stock.action_picking_tree_all").sudo().read()[0]

        if len(pickings) > 1:
            action["domain"] = [("id", "in", pickings.ids)]

        else:
            picking_form_view = self.env.ref("stock.view_picking_form")
            action["views"] = [(picking_form_view.id, "form")]
            action["res_id"] = pickings.id

        return action


def _is_preparation_return_picking(picking):
    """Return whether the given stock picking is a return picking.

    This function allows to partition `Preparation Pickings` from
    `Preparation Return Pickings`.

    The strategy is to check whether the picking type is the picking
    type defined as the preparation return type on the warehouse.
    """
    picking_type = picking.picking_type_id
    return_type_on_warehouse = picking_type.warehouse_id.consu_prep_return_type_id
    return picking_type == return_type_on_warehouse
