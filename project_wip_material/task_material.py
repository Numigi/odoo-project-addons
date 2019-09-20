# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'

    task_id = fields.Many2one('project.task', 'Task')
    project_id = fields.Many2one(related='task_id.project_id', store=True)


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    task_id = fields.Many2one(related='group_id.task_id', store=True)
    project_id = fields.Many2one(related='group_id.project_id', store=True)


class StockMove(models.Model):

    _inherit = 'stock.move'

    task_id = fields.Many2one(related='group_id.task_id', store=True)
    project_id = fields.Many2one(related='group_id.project_id', store=True)
    material_line_id = fields.Many2one(
        'project.task.material',
        'Material Line',
        index=True,
        ondelete='restrict',
    )


class ProcurementRule(models.Model):

    _inherit = 'procurement.rule'

    def _get_stock_move_values(
        self, product_id, product_qty, product_uom,
        location_id, name, origin, values, group_id
    ):
        """Propagate material_line_id from procurement rule to stock move."""
        result = super()._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name,
            origin, values, group_id,
        )
        result['material_line_id'] = values.get('material_line_id')
        return result


class Project(models.Model):
    """Add warehouse to project."""

    _inherit = 'project.project'

    def _get_default_warehouse(self):
        company = self.env.user.company_id
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
        return warehouse

    warehouse_id = fields.Many2one(
        'stock.warehouse', 'Warehouse', ondelete='restrict',
        default=_get_default_warehouse,
    )


class TaskMaterialLine(models.Model):
    """Add material consumption to tasks."""

    _name = 'project.task.material'
    _description = 'Task Material Consumption'
    _order = 'product_id, id'

    company_id = fields.Many2one(related='task_id.company_id', store=True)
    project_id = fields.Many2one(
        'project.project',
        related='task_id.project_id',
        store=True,
        readonly=True,
    )
    task_id = fields.Many2one(
        'project.task', 'Task',
        index=True, required=True,
    )
    product_id = fields.Many2one(
        'product.product', 'Product',
        required=True,
        domain="[('type', 'in', ('product', 'consu'))]",
    )
    initial_qty = fields.Float(
        'Initial Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        required=True,
        default=1.0,
    )
    consumed_qty = fields.Float(
        string='Consumed Quantity',
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_consumed_qty',
    )
    product_uom_id = fields.Many2one(related='product_id.uom_id', readonly=True)
    unit_cost = fields.Float(
        related='product_id.standard_price',
        string='Unit Cost',
        readonly=True,
    )
    move_ids = fields.One2many(
        'stock.move',
        'material_line_id',
        'Stock Moves',
    )

    def _compute_consumed_qty(self):
        for line in self:
            consumed_moves = line.move_ids.filtered(
                lambda m: m.state == 'done' and m.picking_code == 'consumption')
            consumed_qty = sum(consumed_moves.mapped('product_uom_qty'))
            return_moves = line.move_ids.filtered(
                lambda m: m.state == 'done' and m.picking_code == 'consumption_return')
            returned_qty = sum(return_moves.mapped('product_uom_qty'))
            line.consumed_qty = consumed_qty - returned_qty

    def _get_uom_precision(self):
        return self.env['decimal.precision'].precision_get('Product Unit of Measure')

    def _check_date_planned(self):
        if not self.task_id.date_planned:
            raise ValidationError(_(
                'Before adding material to the task, you must set a planned date.'
            ))

    def _check_initial_qty_greater_than_zero(self):
        precision = self._get_uom_precision()
        if float_compare(self.initial_qty, 0, precision_digits=precision) < 0:
            raise ValidationError(_(
                'Material consumption lines can not have an initial quantity below zero. '
                'The line {line} has a quantity of {qty}.'
            ).format(line=self.product_id.display_name, qty=self.initial_qty))

    def _get_consumption_stock_move_qty(self):
        moves_not_cancelled = self.move_ids.filtered(lambda m: m.state != 'cancel')
        return sum(
            m.product_uom_qty if m.picking_code == 'consumption' else -m.product_uom_qty
            for m in moves_not_cancelled
        )

    def _get_warehouse(self):
        if not self.task_id.project_id.warehouse_id:
            raise ValidationError(_(
                'Before adding products to consume on a task, a warehouse must be defined '
                'on the project ({project}).'
            ).format(project=self.task_id.project_id.display_name))
        return self.task_id.project_id.warehouse_id

    def _get_consumption_location(self):
        warehouse = self._get_warehouse()
        if not warehouse.consu_location_id:
            raise ValidationError(_(
                'The warehouse {warehouse} does not have a consumption location.'
            ).format(warehouse=warehouse.display_name))
        return warehouse.consu_location_id

    def _get_consumption_route(self):
        warehouse = self._get_warehouse()
        if not warehouse.consu_route_id:
            raise ValidationError(_(
                'The warehouse {warehouse} does not have a consumption route.'
            ).format(warehouse=warehouse.display_name))
        return warehouse.consu_route_id

    def _get_procurement_values(self):
        date_planned = fields.Date.from_string(self.task_id.date_planned)
        datetime_planned_str = fields.Datetime.to_string(date_planned)
        return {
            'company_id': self.company_id,
            'group_id': self.task_id._get_procurement_group(),
            'date_planned': datetime_planned_str,
            'warehouse_id': self.task_id.project_id.warehouse_id,
            'material_line_id': self.id,
        }

    def _update_procurement_quantities(self):
        """Launch a procurement for the missing quantity on stock moves.

        This method assumes that the initial quantity field is greater than
        the quantity on stock moves.
        """
        move_qty = self._get_consumption_stock_move_qty()
        missing_qty = self.initial_qty - move_qty
        self.env['procurement.group'].run(
            self.product_id,
            missing_qty,
            self.product_uom_id,
            self._get_consumption_location(),
            self.product_id.display_name,
            self.task_id._get_reference_for_procurements(),
            self._get_procurement_values(),
        )

    def _find_reducible_stock_moves(self):
        """Find reducible stock moves related to the material line.

        :rtype: stock.move
        """
        return self.move_ids.filtered(lambda m: (
            m.state not in ('draft', 'done', 'cancel') and
            m.picking_code == 'consumption'
        ))

    def _check_quantity_can_be_reduced(self):
        """Check that the initial_qty can be reduced to the new value."""
        total_move_qty = self._get_consumption_stock_move_qty()

        reducible_moves = self._find_reducible_stock_moves()
        reducible_qty = sum(reducible_moves.mapped('product_uom_qty'))

        quantity_to_reduce = total_move_qty - self.initial_qty

        precision = self._get_uom_precision()
        more_to_reduce_than_available = (
            float_compare(quantity_to_reduce, reducible_qty, precision_digits=precision) > 0
        )
        if more_to_reduce_than_available:
            raise ValidationError(_(
                'The quantity on the material line {line} can not be reduced to {new_quantity} '
                '(it can not be lower than the delivered quantity).\n\n'
                'The line may not be reduced below a minimum of {minimum_qty} {uom}.'
            ).format(
                line=self.product_id.display_name,
                new_quantity=self.initial_qty,
                minimum_qty=total_move_qty - reducible_qty,
                uom=self.product_uom_id.name,
            ))

    def _cancel_moves_with_zero_quantity(self):
        """Cancel the stock moves related to this line with zero quantity.

        Also unlink these stock moves from their respective picking.
        This allows when removing a material line, to hide stock moves
        with zero quantity. Otherwise, stock moves with zero quantity
        would appear in pickings and create confusion among users.
        """
        self.move_ids

        moves = self.move_ids
        limit = 10
        while moves and limit:
            moves_with_zero_qty = moves.filtered(lambda m: m.product_qty == 0)
            moves = moves_with_zero_qty.mapped('move_orig_ids')

            moves_with_zero_qty._action_cancel()
            moves_with_zero_qty.write({'picking_id': False})
            limit -= 1

    def _run_procurements(self):
        """Generate procurements for the material line.

        Generate any required stock move (using procurements).

        Reduce the quantity on existing stock moves if it exceeds the initial quantity
        on the material line.
        """
        self._check_date_planned()
        self._check_initial_qty_greater_than_zero()

        precision = self._get_uom_precision()

        move_qty = self._get_consumption_stock_move_qty()
        more_move_qty_than_required = (
            float_compare(move_qty, self.initial_qty, precision_digits=precision) > 0
        )

        if more_move_qty_than_required:
            self._check_quantity_can_be_reduced()

        self._update_procurement_quantities()

        if more_move_qty_than_required:
            self._cancel_moves_with_zero_quantity()

    @api.model
    def create(self, vals):
        """Generate procurements when adding a new material line.

        The sudo is required, because project users do not have access to stock objects.
        """
        line = super().create(vals)
        line.sudo()._run_procurements()
        return line

    @api.multi
    def write(self, vals):
        """Adjust procurements when modifying the quantity on a material line.

        The sudo is required, because project users do not have access to stock objects.
        """
        if 'product_id' in vals:
            raise ValidationError(_(
                'You may not change the product on an existing material line. '
                'Instead of changing the product, you may '
                'delete the line and create a new one.'
            ))

        super().write(vals)

        if 'initial_qty' in vals:
            for line in self:
                line.sudo()._run_procurements()

        return True

    def _cancel_procurements_for_line_to_delete(self):
        any_stock_move_done = any((m.state == 'done' for m in self.move_ids))

        if any_stock_move_done:
            raise ValidationError(_(
                'The material line {line} can not be deleted because '
                'it is bound to stock moves with the status done.'
            ).format(line=self.product_id.display_name))

        self.initial_qty = 0
        self._run_procurements()
        self.move_ids.write({'material_line_id': False})

    @api.multi
    def unlink(self):
        """Cancel procurements when deleting material line.

        The sudo is required, because project users do not have access to stock objects.
        """
        for line in self:
            line.sudo()._cancel_procurements_for_line_to_delete()
        return super().unlink()


class TaskMaterialWithProjectSelect(models.Model):
    """Add a technical computed field to allow constrain the domain when selecting the task.

    This field is not stored and only used as a helper in the global list view of material.
    """

    _inherit = 'project.task.material'

    project_select_id = fields.Many2one(
        'project.project',
        'Project Select',
        compute='_compute_project_select',
        inverse=lambda self: None,
    )

    def _compute_project_select(self):
        for material in self:
            material.project_select_id = material.project_id

    @api.onchange('project_select_id')
    def _onchange_project_select_reset_task(self):
        if self.project_select_id != self.task_id.project_id:
            self.task_id = False


class Task(models.Model):
    """Add material consumption to tasks."""

    _inherit = 'project.task'

    material_line_ids = fields.One2many(
        'project.task.material',
        'task_id',
        'Material',
    )

    procurement_group_id = fields.Many2one(
        'procurement.group', 'Procurement Group',
        copy=False,
    )

    def _get_reference_for_procurements(self):
        return 'TA#{}'.format(str(self.id))

    def _get_procurement_group(self):
        if not self.procurement_group_id:
            self.procurement_group_id = self.env['procurement.group'].create({
                'name': self._get_reference_for_procurements(),
                'task_id': self.id,
            })
        return self.procurement_group_id

    def _propagate_planned_date_to_stock_moves(self):
        moves_to_update = self.mapped('material_line_ids.move_ids').filtered(
            lambda m: m.state not in ('done', 'cancel'))
        moves_to_update.write({'date_expected': self.date_planned})

    def write(self, vals):
        """When changing the planned date, propagate the new value to stock moves."""
        super().write(vals)

        if 'date_planned' in vals:
            for task in self:
                task._propagate_planned_date_to_stock_moves()

        return True
