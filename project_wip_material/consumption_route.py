# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, SUPERUSER_ID, _

ONE_STEP_DESCRIPTION = "Direct consumption from stocks (1 step)"


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
        return self.env.ref('stock.location_production', raise_if_not_found=False).id,

    consu_steps = fields.Selection([
        ('one_step', ONE_STEP_DESCRIPTION),
    ], default='one_step', required=True)

    consu_location_id = fields.Many2one(
        'stock.location', 'Consumption Location',
        domain=[('usage', '=', 'production')],
        ondelete='restrict',
        required=True,
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
            'code': 'consumption',
            'default_location_src_id': self.lot_stock_id.id,
            'default_location_dest_id': self.consu_location_id.id,
        }

    def _get_consumption_return_picking_type_values(self):
        return {
            'code': 'consumption_return',
            'default_location_src_id': self.consu_location_id.id,
            'default_location_dest_id': self.lot_stock_id.id,
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
        return {
            'name': self._format_rulename(self.lot_stock_id, self.consu_location_id, 'Production'),
            'location_src_id': self.lot_stock_id.id,
            'location_id': self.consu_location_id.id,
            'picking_type_id': self.consu_type_id.id,
            'action': 'move',
            'active': True,
            'company_id': self.company_id.id,
        }

    def _get_consumption_route_values(self):
        return {
            'name': "{warehouse}: {description}".format(
                warehouse=self.name,
                description=_(ONE_STEP_DESCRIPTION),
            ),
            'pull_ids': [
                (5, 0),
                (0, 0, self._get_consumption_pull_values()),
            ],
            'active': True,
            'company_id': self.company_id.id,
            'product_categ_selectable': True,
            'warehouse_selectable': True,
            'product_selectable': False,
            'sequence': 10,
        }

    def _create_consumption_route(self):
        vals = self._get_consumption_route_values()
        self.consu_route_id = self.env['stock.location.route'].create(vals)

    def _update_consumption_route(self):
        vals = self._get_consumption_route_values()
        self.consu_route_id.write(vals)

    def _create_or_update_consumption_route(self):
        if self.consu_route_id:
            self._update_consumption_route()
        else:
            self._create_consumption_route()

    @api.model
    def create(self, vals):
        warehouse = super().create(vals)
        warehouse._create_consumption_picking_types()
        warehouse._create_consumption_route()
        return warehouse

    @api.multi
    def write(self, vals):
        super().write(vals)
        if 'consu_steps' in vals:
            for warehouse in self:
                warehouse._create_or_update_consumption_picking_types()
                warehouse._create_or_update_consumption_route()
        return True


def _update_warehouses_consumption_routes(cr, registry):
    """Init hook for updating stock routes after the module is installed."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    warehouses = env['stock.warehouse'].search([])
    for warehouse in warehouses:
        warehouse._create_or_update_consumption_picking_types()
        warehouse._create_or_update_consumption_route()
