# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import timedelta
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class TaskMaterialLine(models.Model):

    _name = "project.task.material"
    _description = "Task Material Consumption"
    _order = "product_id, id"
    _inherit = "project.select.mixin"

    company_id = fields.Many2one(related="task_id.company_id", store=True)
    project_id = fields.Many2one(
        "project.project", related="task_id.project_id", store=True, readonly=True
    )
    task_id = fields.Many2one("project.task", "Task", index=True, required=True)
    product_id = fields.Many2one(
        "product.product",
        "Product",
        required=True,
        domain="[('type', 'in', ('product', 'consu'))]",
    )
    initial_qty = fields.Float(
        "Initial Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        required=True,
        default=1.0,
    )
    prepared_qty = fields.Float(
        string="Prepared Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_prepared_qty",
        store=True,
        compute_sudo=True,
    )
    consumed_qty = fields.Float(
        string="Consumed Quantity",
        digits=dp.get_precision("Product Unit of Measure"),
        compute="_compute_consumed_qty",
        store=True,
        compute_sudo=True,
    )
    product_uom_id = fields.Many2one(related="product_id.uom_id", readonly=True)
    unit_cost = fields.Float(
        related="product_id.standard_price", string="Unit Cost", readonly=True
    )
    move_ids = fields.One2many("stock.move", "material_line_id", "Stock Moves")

    @api.depends(
        "move_ids.move_orig_ids",
        "move_ids.move_orig_ids.state",
        "move_ids.move_orig_ids.returned_move_ids",
        "move_ids.move_orig_ids.returned_move_ids.state",
    )
    def _compute_prepared_qty(self):
        for line in self:
            preparation_moves = line.mapped("move_ids.move_orig_ids")
            preparation_moves_done = preparation_moves.filtered(
                lambda m: m.state == "done"
            )
            prepared_qty = sum(preparation_moves_done.mapped("product_uom_qty"))
            return_moves = preparation_moves_done.mapped("returned_move_ids")
            return_moves_done = return_moves.filtered(lambda m: m.state == "done")
            returned_qty = sum(return_moves_done.mapped("product_uom_qty"))
            line.prepared_qty = prepared_qty - returned_qty

    @api.depends("move_ids", "move_ids.state")
    def _compute_consumed_qty(self):
        for line in self:
            consumed_moves = line.move_ids.filtered(
                lambda m: m.state == "done" and m.picking_code == "consumption"
            )
            consumed_qty = sum(consumed_moves.mapped("product_uom_qty"))
            return_moves = line.move_ids.filtered(
                lambda m: m.state == "done" and m.picking_code == "consumption_return"
            )
            returned_qty = sum(return_moves.mapped("product_uom_qty"))
            line.consumed_qty = consumed_qty - returned_qty

    @api.model
    def create(self, vals):
        """Generate procurements when adding a new material line.

        The sudo is required, because project users do not have access to stock objects.
        """
        line = super().create(vals)
        if line._should_generate_procurement():
            line.sudo()._run_procurements()
        return line

    @api.multi
    def write(self, vals):
        """Adjust procurements when modifying the quantity on a material line.

        The sudo is required, because project users do not have access to stock objects.
        """
        if "product_id" in vals or "task_id" in vals:
            for line in self:
                line.sudo()._check_can_change_product_or_task()
                line.sudo()._cancel_procurements()

        super().write(vals)

        if "product_id" in vals or "task_id" in vals or "initial_qty" in vals:
            lines_with_procurement = self.filtered(
                lambda l: l._should_generate_procurement()
            )
            for line in lines_with_procurement:
                line.sudo()._run_procurements()

        return True

    @api.multi
    def unlink(self):
        """Cancel procurements when deleting material line.

        The sudo is required, because project users do not have access to stock objects.
        """
        for line in self:
            line.sudo()._check_line_can_be_deleted()
            line.sudo()._cancel_procurements()
        return super().unlink()

    def _should_generate_procurement(self):
        return True

    def _cancel_procurements(self):
        self.initial_qty = 0
        self._run_procurements()
        self.move_ids.write({"material_line_id": False})

    def _run_procurements(self):
        """Generate procurements for the material line.

        Generate any required stock move (using procurements).

        Reduce the quantity on existing stock moves if it exceeds the initial quantity
        on the material line.
        """
        self._check_date_planned()
        self._check_initial_qty_greater_than_zero()

        self._check_quantity_can_be_reduced()

        self._update_procurement_quantities()
        self._cancel_moves_with_zero_quantity()

    def _check_date_planned(self):
        if not self.task_id.date_planned:
            raise ValidationError(
                _("Before adding material to the task, you must set a planned date.")
            )

    def _check_initial_qty_greater_than_zero(self):
        precision = self._get_uom_precision()
        if float_compare(self.initial_qty, 0, precision_digits=precision) < 0:
            raise ValidationError(
                _(
                    "Material consumption lines can not have an initial quantity below zero. "
                    "The line {line} has a quantity of {qty}."
                ).format(line=self.product_id.display_name, qty=self.initial_qty)
            )

    def _update_procurement_quantities(self):
        """Launch a procurement for the missing quantity on stock moves.

        This method assumes that the initial quantity field is greater than
        the quantity on stock moves.
        """
        move_qty = self._get_total_move_qty()
        missing_qty = self.initial_qty - move_qty
        self.env["procurement.group"].run(
            self.product_id,
            missing_qty,
            self.product_uom_id,
            self._get_consumption_location(),
            self.product_id.display_name,
            self.task_id._get_reference_for_procurements(),
            self._get_procurement_values(),
        )

    def _get_consumption_location(self):
        warehouse = self._get_warehouse()
        if not warehouse.consu_location_id:
            raise ValidationError(
                _(
                    "The warehouse {warehouse} does not have a consumption location."
                ).format(warehouse=warehouse.display_name)
            )
        return warehouse.consu_location_id

    def _get_warehouse(self):
        if not self.task_id.project_id.warehouse_id:
            raise ValidationError(
                _(
                    "Before adding products to consume on a task, a warehouse must be defined "
                    "on the project ({project})."
                ).format(project=self.task_id.project_id.display_name)
            )
        return self.task_id.project_id.warehouse_id

    def _get_procurement_values(self):
        date_planned = fields.Date.from_string(self.task_id.date_planned)
        datetime_planned_str = fields.Datetime.to_string(date_planned)
        return {
            "company_id": self.company_id,
            "group_id": self.task_id._get_procurement_group(),
            "date_planned": datetime_planned_str,
            "warehouse_id": self.task_id.project_id.warehouse_id,
            "material_line_id": self.id,
            "task_id": self.task_id.id,
        }

    def _check_quantity_can_be_reduced(self):
        """Check that the initial_qty can be reduced to the new value."""
        total_move_qty = self._get_total_move_qty()

        reducible_moves = self._find_reducible_stock_moves()
        reducible_qty = sum(reducible_moves.mapped("product_uom_qty"))

        quantity_to_reduce = total_move_qty - self.initial_qty

        precision = self._get_uom_precision()
        more_to_reduce_than_available = (
            float_compare(quantity_to_reduce, reducible_qty, precision_digits=precision)
            > 0
        )
        if more_to_reduce_than_available:
            raise ValidationError(
                _(
                    "The quantity on the material line {line} can not be reduced to {new_quantity} "
                    "(it can not be lower than the delivered quantity).\n\n"
                    "The line may not be reduced below a minimum of {minimum_qty} {uom}."
                ).format(
                    line=self.product_id.display_name,
                    new_quantity=self.initial_qty,
                    minimum_qty=total_move_qty - reducible_qty,
                    uom=self.product_uom_id.name,
                )
            )

    def _check_can_change_product_or_task(self):
        if self._has_any_stock_move_done():
            raise ValidationError(
                _(
                    "You may not change the product or the task on "
                    "the material line {line} because "
                    "it is bound to stock moves with the status done."
                ).format(line=self.product_id.display_name)
            )

    def _check_line_can_be_deleted(self):
        if self._has_any_stock_move_done():
            raise ValidationError(
                _(
                    "The material line {line} can not be deleted because "
                    "it is bound to stock moves with the status done."
                ).format(line=self.product_id.display_name)
            )

    def _has_any_stock_move_done(self):
        """Return whether the material line has any stock move at the state done."""
        return any((m.state == "done" for m in self.mapped("move_ids")))

    def _find_reducible_stock_moves(self):
        """Find reducible stock moves related to the material line.

        :rtype: stock.move
        """
        return self._get_first_step_moves().filtered(
            lambda m: m.state not in ("done", "cancelled")
        )

    def _get_total_move_qty(self):
        moves = self._get_first_step_moves()
        return sum(
            moves.filtered(lambda m: m.state != "cancel").mapped("product_uom_qty")
        )

    def _get_first_step_moves(self):
        moves = self.env["stock.move"]

        for moves in self._iter_procurement_moves():
            pass

        return moves

    def _cancel_moves_with_zero_quantity(self):
        """Cancel the stock moves related to this line with zero quantity.

        Also unlink these stock moves from their respective picking.
        This allows when removing a material line, to hide stock moves
        with zero quantity. Otherwise, stock moves with zero quantity
        would appear in pickings and create confusion among users.
        """
        for moves in self._iter_procurement_moves():
            moves_with_zero_qty = moves.filtered(lambda m: m.product_qty == 0)
            moves_with_zero_qty._action_cancel()
            moves_with_zero_qty.write({"picking_id": False})

    def _propagate_planned_date_to_stock_moves(self):
        date_planned = self.task_id.date_planned

        for moves in self._iter_procurement_moves():
            moves_to_update = moves.filtered(
                lambda m: m.state not in ("done", "cancel")
            )

            delay = moves_to_update.mapped("rule_id.delay")
            if delay:
                date_planned = date_planned - timedelta(delay[0])

            moves_to_update.with_context(do_not_propagate=True).write(
                {"date_expected": date_planned}
            )

    def _iter_procurement_moves(self):
        moves = self.move_ids

        # Limit the recursion depth stock.move chains.
        # A chain of more than 3 moves is unlikely.
        limit = 10

        while moves and limit:
            origin_moves = moves.mapped("move_orig_ids")
            yield moves
            moves = origin_moves
            limit -= 1

    def _get_uom_precision(self):
        return self.env["decimal.precision"].precision_get("Product Unit of Measure")
