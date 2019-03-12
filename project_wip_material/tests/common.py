# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests import common


class TaskMaterialCase(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({
            'name': 'Test Company',
        })
        cls.warehouse = cls.env['stock.warehouse'].search([
            ('company_id', '=', cls.company.id),
        ], limit=1)
        cls.route = cls.warehouse.consu_route_id

        cls.journal = cls.env['account.journal'].create({
            'name': 'Stock Journal',
            'type': 'general',
            'code': 'STOCK',
        })

        cls.stock_account = cls.env['account.account'].create({
            'name': 'Raw Material Stocks',
            'code': '130101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
        })

        cls.wip_account = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140101',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'reconcile': True,
        })

        cls.product_category = cls.env['product.category'].create({
            'name': 'Category 1',
            'property_valuation': 'real_time',
            'property_cost_method': 'standard',
            'property_stock_journal': cls.journal.id,
            'property_stock_valuation_account_id': cls.stock_account.id,
        })

        cls.project_type = cls.env['project.type'].create({
            'name': 'Trailer Refurb',
            'wip_account_id': cls.wip_account.id,
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Job 123',
            'warehouse_id': cls.warehouse.id,
            'project_type_id': cls.project_type.id,
        })
        cls.task = cls.env['project.task'].create({
            'name': 'Task 450',
            'project_id': cls.project.id,
            'date_planned': datetime.now(),
        })

        cls.product_a_value = 50
        cls.product_a = cls.env['product.product'].create({
            'name': 'Product A',
            'type': 'product',
            'standard_price': cls.product_a_value,
            'categ_id': cls.product_category.id,
        })
        cls.product_b_value = 100
        cls.product_b = cls.env['product.product'].create({
            'name': 'Product B',
            'type': 'product',
            'standard_price': cls.product_b_value,
            'categ_id': cls.product_category.id,
        })

    @classmethod
    def _create_material_line(cls, task=None, product=None, initial_qty=1):
        return cls.env['project.task.material'].create({
            'task_id': task.id if task else cls.task.id,
            'product_id': product.id if product else cls.product_a.id,
            'initial_qty': initial_qty,
        })

    @classmethod
    def _force_transfer_move(cls, move, quantity=None):
        move.move_line_ids |= cls.env['stock.move.line'].create(dict(
            move._prepare_move_line_vals(), qty_done=quantity or move.product_uom_qty))
        move.picking_id.action_done()

    @classmethod
    def _return_stock_move(cls, move_to_return, returned_qty):
        """Return the given stock move.

        :param move_to_return: the stock move to return
        :param returned_qty: the quantity to return
        """
        wizard_fields = [
            'product_return_moves',
            'move_dest_exists',
            'parent_location_id',
            'original_location_id',
            'location_id',
        ]
        wizard_cls = cls.env['stock.return.picking'].with_context(
            active_id=move_to_return.picking_id.id
        )
        wizard_defaults = wizard_cls.default_get(wizard_fields)
        wizard = wizard_cls.create(wizard_defaults)

        for product_return in wizard.product_return_moves:
            if product_return.move_id == move_to_return:
                product_return.quantity = returned_qty

        return_picking_id = wizard.create_returns()['res_id']
        return_picking = cls.env['stock.picking'].browse(return_picking_id)
        cls._force_transfer_move(return_picking.move_lines)
        return return_picking.move_lines
