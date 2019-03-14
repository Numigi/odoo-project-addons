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
        cls.project_user = cls.env['res.users'].create({
            'name': 'Project User',
            'login': 'project_user',
            'email': 'project_user@test.com',
            'group_id': [(4, cls.env.ref('project.group_project_user').id)],
            'company_id': cls.company.id,
            'company_ids': [(4, cls.company.id)],
        })
        cls.stock_user = cls.env['res.users'].create({
            'name': 'Stock User',
            'login': 'stock_user',
            'email': 'stock_user@test.com',
            'group_id': [(4, cls.env.ref('stock.group_stock_user').id)],
            'company_id': cls.company.id,
            'company_ids': [(4, cls.company.id)],
        })

    @classmethod
    def _create_material_line(cls, task=None, product=None, initial_qty=1):
        """Create a new material line.

        Use project user to create the line to verify that no access error is raised.
        Return the material lines with sudo priviledges for assertions.
        """
        new_line = cls.env['project.task.material'].sudo(cls.project_user).create({
            'task_id': task.id if task else cls.task.id,
            'product_id': product.id if product else cls.product_a.id,
            'initial_qty': initial_qty,
        })
        return new_line.sudo()

    @classmethod
    def _force_transfer_move(cls, move, quantity=None):
        """Force the transfer of a stock move.

        Use stock user to transfer the move to verify that no access error is raised.
        """
        move.move_line_ids |= (
            cls.env['stock.move.line'].sudo(cls.stock_user)
            .create(dict(move._prepare_move_line_vals(), qty_done=quantity or move.product_uom_qty))
        )
        move.picking_id.action_done()

    @classmethod
    def _return_stock_move(cls, move_to_return, returned_qty):
        """Return the given stock move.

        Use stock user to transfer the move to verify that no access error is raised.
        Return the stock moves with sudo priviledges for assertions.

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
        wizard_cls = cls.env['stock.return.picking'].sudo(cls.stock_user).with_context(
            active_id=move_to_return.picking_id.id
        )
        wizard_defaults = wizard_cls.default_get(wizard_fields)
        wizard = wizard_cls.create(wizard_defaults)

        for product_return in wizard.product_return_moves:
            if product_return.move_id == move_to_return:
                product_return.quantity = returned_qty

        return_picking_id = wizard.create_returns()['res_id']
        return_picking = cls.env['stock.picking'].sudo(cls.stock_user).browse(return_picking_id)
        cls._force_transfer_move(return_picking.move_lines)
        return return_picking.move_lines.sudo()
