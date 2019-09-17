# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, SUPERUSER_ID, _


ONE_STEP_KEY = "one_step"
ONE_STEP_DESCRIPTION = _("Direct consumption from stocks (1 step)")


def _has_one_step_consumption(warehouse: 'StockWarehouse'):
    return warehouse.consu_steps == ONE_STEP_KEY


class StockPickingType(models.Model):
    """Add consumption to picking type codes."""

    _inherit = 'stock.picking.type'

    code = fields.Selection(selection_add=[
        ('consumption', 'Consumption'),
        ('consumption_return', 'Consumption Return'),
    ])


class Warehouse(models.Model):
    """Add consumption route to the warehouse."""

    _inherit = 'stock.warehouse'

    def _get_default_consumption_location_id(self):
        return self.env.ref('stock.location_production', raise_if_not_found=False).id

    consu_steps = fields.Selection([
        (ONE_STEP_KEY, ONE_STEP_DESCRIPTION),
    ], default=ONE_STEP_KEY)

    consu_location_id = fields.Many2one(
        'stock.location', 'Consumption Location',
        domain=[('usage', '=', 'production')],
        ondelete='restrict',
        default=_get_default_consumption_location_id,
    )

    consu_type_id = fields.Many2one(
        'stock.picking.type', 'Consumption Picking Type',
        ondelete='restrict',
    )

    consu_return_type_id = fields.Many2one(
        'stock.picking.type', 'Consumption Return Picking Type',
        ondelete='restrict',
    )

    consu_route_id = fields.Many2one(
        'stock.location.route', 'Consumption Route',
        ondelete='restrict',
    )

    def _get_consumption_sequence_values(self):
        return {
            'name': '{}: Consumption'.format(self.name),
            'prefix': '{}/CO/'.format(self.code),
            'padding': 5,
        }

    def _get_consumption_return_sequence_values(self):
        return {
            'name': '{}: Consumption Return'.format(self.name),
            'prefix': '{}/COR/'.format(self.code),
            'padding': 5,
        }

    def _create_consumption_sequence(self):
        vals = self._get_consumption_sequence_values()
        return self.env['ir.sequence'].create(vals)

    def _create_consumption_return_sequence(self):
        vals = self._get_consumption_return_sequence_values()
        return self.env['ir.sequence'].create(vals)

    def _get_consumption_picking_type_values(self):
        return {
            'warehouse_id': self.id,
            'code': 'consumption',
            'default_location_src_id': (
                self.lot_stock_id.id if _has_one_step_consumption(self) else
                self.consu_prep_location_id.id
            ),
            'default_location_dest_id': self.consu_location_id.id,
        }

    def _get_consumption_return_picking_type_values(self):
        return {
            'warehouse_id': self.id,
            'code': 'consumption_return',
            'default_location_src_id': self.consu_location_id.id,
            'default_location_dest_id': (
                self.lot_stock_id.id if _has_one_step_consumption(self) else
                self.consu_prep_location_id.id
            ),
        }

    def _get_consumption_picking_type_create_values(self):
        vals = self._get_consumption_picking_type_values()
        vals.update({
            'name': _('Consumption'),
            'use_create_lots': True,
            'use_existing_lots': True,
            'sequence': 100,
            'sequence_id': self._create_consumption_sequence().id,
        })
        return vals

    def _get_consumption_return_picking_type_create_values(self):
        vals = self._get_consumption_return_picking_type_values()
        vals.update({
            'name': _('Consumption Return'),
            'use_create_lots': False,
            'use_existing_lots': False,
            'sequence': 101,
            'sequence_id': self._create_consumption_return_sequence().id,
        })
        return vals

    def _bind_consumption_picking_types(self):
        self.consu_type_id.return_picking_type_id = self.consu_return_type_id
        self.consu_return_type_id.return_picking_type_id = self.consu_type_id

    def _create_consumption_picking_types(self):
        vals = self._get_consumption_picking_type_create_values()
        self.consu_type_id = self.env['stock.picking.type'].create(vals)

        vals = self._get_consumption_return_picking_type_create_values()
        self.consu_return_type_id = self.env['stock.picking.type'].create(vals)

        self._bind_consumption_picking_types()

    def _update_consumption_picking_types(self):
        vals = self._get_consumption_picking_type_values()
        self.consu_type_id.write(vals)

        vals = self._get_consumption_return_picking_type_values()
        self.consu_return_type_id.write(vals)

        self._bind_consumption_picking_types()

    def _create_or_update_consumption_picking_types(self):
        if self.consu_type_id:
            self._update_consumption_picking_types()
        else:
            self._create_consumption_picking_types()

    def _get_consumption_pull_values(self):
        source_location = (
            self.lot_stock_id if _has_one_step_consumption(self) else self.consu_prep_location_id
        )
        procure_method = 'make_to_stock' if _has_one_step_consumption(self) else 'make_to_order'
        return {
            'name': self._format_rulename(source_location, self.consu_location_id, ''),
            'location_src_id': source_location.id,
            'location_id': self.consu_location_id.id,
            'picking_type_id': self.consu_type_id.id,
            'action': 'move',
            'active': True,
            'company_id': self.company_id.id,
            'sequence': 1,
            'propagate': True,
            'procure_method': procure_method,
            'group_propagation_option': 'propagate',
        }

    def _get_consumption_route_description(self):
        return _(ONE_STEP_DESCRIPTION)

    def _get_consumption_route_values(self):
        return {
            'name': "{warehouse}: {description}".format(
                warehouse=self.name,
                description=self._get_consumption_route_description(),
            ),
            'active': True,
            'company_id': self.company_id.id,
            'product_categ_selectable': True,
            'warehouse_selectable': True,
            'product_selectable': False,
            'sequence': 10,
            'warehouse_ids': [(4, self.id)],
        }

    def _create_consumption_route(self):
        vals = self._get_consumption_route_values()
        vals['pull_ids'] = [
            (0, 0, self._get_consumption_pull_values()),
        ]
        self.consu_route_id = self.env['stock.location.route'].create(vals)

    def _update_consumption_pull(self):
        existing_pull = self.consu_route_id.pull_ids.filtered(
            lambda p: p.location_id == self.consu_location_id)

        if existing_pull:
            existing_pull.write(self._get_consumption_pull_values())
        else:
            self.consu_route_id.write({'pull_ids': [(0, 0, self._get_consumption_pull_values())]})

    def _update_consumption_route(self):
        vals = self._get_consumption_route_values()
        self.consu_route_id.write(vals)
        self.consu_route_id.pull_ids.write({'active': False})
        self._update_consumption_pull()

    def _create_or_update_consumption_route(self):
        if self.consu_route_id:
            self._update_consumption_route()
        else:
            self._create_consumption_route()

    @api.model
    def create(self, vals):
        """When creating a new warehouse, create the consumption route.

        Use sudo to prevent errors related to access rights.
        """
        warehouse = super().create(vals)
        warehouse.sudo()._create_consumption_picking_types()
        warehouse.sudo()._create_consumption_route()
        return warehouse

    @api.multi
    def write(self, vals):
        """When changing the consumation steps, update the consumption route.

        Use sudo to prevent errors related to access rights.
        """
        super().write(vals)
        if 'consu_steps' in vals:
            for warehouse in self:
                warehouse.sudo()._create_or_update_consumption_picking_types()
                warehouse.sudo()._create_or_update_consumption_route()
        return True


TWO_STEPS_KEY = "two_steps"
TWO_STEPS_DESCRIPTION = _("Prepare the stock before consumption (2 steps)")


def _has_two_steps_consumption(warehouse: 'StockWarehouse'):
    return warehouse.consu_steps == TWO_STEPS_KEY


class WarehouseWithPickingStep(models.Model):
    """Add picking step to the consumption route."""

    _inherit = 'stock.warehouse'

    consu_steps = fields.Selection(selection_add=[(TWO_STEPS_KEY, TWO_STEPS_DESCRIPTION)])

    consu_prep_location_id = fields.Many2one(
        'stock.location', 'Preparation Picking Location',
        domain=[('usage', '=', 'internal')],
        ondelete='restrict',
    )

    consu_prep_type_id = fields.Many2one(
        'stock.picking.type', 'Preparation Picking Type',
        ondelete='restrict',
    )

    consu_prep_return_type_id = fields.Many2one(
        'stock.picking.type', 'Preparation Return Picking Type',
        ondelete='restrict',
    )

    def _get_consumption_route_description(self):
        return (
            _(TWO_STEPS_DESCRIPTION) if _has_two_steps_consumption(self) else
            super()._get_consumption_route_description()
        )

    def _get_consumption_prep_sequence_values(self):
        return {
            'name': '{}: Consumption Preparation'.format(self.name),
            'prefix': '{}/PR/'.format(self.code),
            'padding': 5,
        }

    def _get_consumption_prep_return_sequence_values(self):
        return {
            'name': '{}: Consumption Preparation Return'.format(self.name),
            'prefix': '{}/PRR/'.format(self.code),
            'padding': 5,
        }

    def _create_consumption_prep_sequence(self):
        vals = self._get_consumption_prep_sequence_values()
        return self.env['ir.sequence'].create(vals)

    def _create_consumption_prep_return_sequence(self):
        vals = self._get_consumption_prep_return_sequence_values()
        return self.env['ir.sequence'].create(vals)

    def _get_consumption_prep_picking_type_values(self):
        return {
            'warehouse_id': self.id,
            'code': 'internal',
            'default_location_src_id': self.lot_stock_id.id,
            'default_location_dest_id': self.consu_prep_location_id.id,
        }

    def _get_consumption_prep_return_picking_type_values(self):
        return {
            'warehouse_id': self.id,
            'code': 'internal',
            'default_location_src_id': self.consu_prep_location_id.id,
            'default_location_dest_id': self.lot_stock_id.id,
        }

    def _get_consumption_prep_picking_type_create_values(self):
        vals = self._get_consumption_prep_picking_type_values()
        vals.update({
            'name': _('Preparation'),
            'use_create_lots': True,
            'use_existing_lots': True,
            'sequence': 100,
            'sequence_id': self._create_consumption_prep_sequence().id,
        })
        return vals

    def _get_consumption_prep_return_picking_type_create_values(self):
        vals = self._get_consumption_prep_return_picking_type_values()
        vals.update({
            'name': _('Preparation Return'),
            'use_create_lots': False,
            'use_existing_lots': False,
            'sequence': 101,
            'sequence_id': self._create_consumption_prep_return_sequence().id,
        })
        return vals

    def _bind_consumption_prep_picking_types(self):
        self.consu_prep_type_id.return_picking_type_id = self.consu_prep_return_type_id
        self.consu_prep_return_type_id.return_picking_type_id = self.consu_prep_type_id

    def _create_consumption_prep_picking_types(self):
        vals = self._get_consumption_prep_picking_type_create_values()
        self.consu_prep_type_id = self.env['stock.picking.type'].create(vals)

        vals = self._get_consumption_prep_return_picking_type_create_values()
        self.consu_prep_return_type_id = self.env['stock.picking.type'].create(vals)

        self._bind_consumption_prep_picking_types()

    def _update_consumption_prep_picking_types(self):
        vals = self._get_consumption_prep_picking_type_values()
        self.consu_prep_type_id.write(vals)

        vals = self._get_consumption_prep_return_picking_type_values()
        self.consu_prep_return_type_id.write(vals)

        self._bind_consumption_prep_picking_types()

    def _create_or_update_consumption_picking_types(self):
        super()._create_or_update_consumption_picking_types()

        require_prep_type = _has_two_steps_consumption(self)

        if require_prep_type and self.consu_prep_type_id:
            self._update_consumption_prep_picking_types()

        elif require_prep_type:
            self._create_consumption_prep_picking_types()

    def _get_consumption_prep_pull_values(self):
        return {
            'name': self._format_rulename(self.lot_stock_id, self.consu_prep_location_id, ''),
            'location_src_id': self.lot_stock_id.id,
            'location_id': self.consu_prep_location_id.id,
            'picking_type_id': self.consu_prep_type_id.id,
            'action': 'move',
            'active': True,
            'company_id': self.company_id.id,
            'sequence': 2,
            'propagate': True,
            'procure_method': 'make_to_stock',
            'group_propagation_option': 'propagate',
        }

    def _create_consumption_route(self):
        super()._create_consumption_route()
        if _has_two_steps_consumption(self):
            self.consu_route_id.write({
                'pull_ids': [(0, 0, self._get_consumption_prep_pull_values())],
            })

    def _update_consumption_prep_pull(self):
        existing_pull = self.consu_route_id.pull_ids.filtered(
            lambda p: p.location_id == self.consu_prep_location_id)

        pull_required = _has_two_steps_consumption(self)

        if existing_pull and pull_required:
            existing_pull.write(self._get_consumption_prep_pull_values())

        if existing_pull and not pull_required:
            existing_pull.active = False

        if not existing_pull and pull_required:
            self.consu_route_id.write({
                'pull_ids': [(0, 0, self._get_consumption_prep_pull_values())],
            })

    def _update_consumption_route(self):
        super()._update_consumption_route()
        self._update_consumption_prep_pull()


def _update_warehouses_consumption_routes(cr, registry):
    """Init hook for updating stock routes after the module is installed."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    warehouses = env['stock.warehouse'].search([])
    for warehouse in warehouses:
        warehouse._create_or_update_consumption_picking_types()
        warehouse._create_or_update_consumption_route()
