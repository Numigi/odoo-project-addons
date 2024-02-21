# Copyright 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests import common
from odoo.tests.common import Form


class TaskMaterialCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create({"name": "Test Company 2"})
        cls.manager = cls.env["res.users"].create(
            {
                "name": "Manager",
                "login": "manager",
                "email": "manager@test.com",
                "groups_id": [
                    (4, cls.env.ref("project.group_project_manager").id),
                    (4, cls.env.ref("stock.group_stock_manager").id),
                ],
                "company_id": cls.company.id,
                "company_ids": [(4, cls.company.id)],
            }
        )
        cls.project_user = cls.env["res.users"].create(
            {
                "name": "Project User",
                "login": "project_user",
                "email": "project_user@test.com",
                "groups_id": [(4, cls.env.ref("project.group_project_user").id)],
                "company_id": cls.company.id,
                "company_ids": [(4, cls.company.id)],
            }
        )
        cls.stock_user = cls.env["res.users"].create(
            {
                "name": "Stock User",
                "login": "stock_user",
                "email": "stock_user@test.com",
                "groups_id": [(4, cls.env.ref("stock.group_stock_user").id)],
                "company_id": cls.company.id,
                "company_ids": [(4, cls.company.id)],
            }
        )

        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)], limit=1
        )
        cls.warehouse.consu_prep_location_id = cls.env["stock.location"].create(
            {
                "name": "Preparation",
                "usage": "internal",
                "location_id": cls.warehouse.view_location_id.id,
                "company_id": cls.company.id,
            }
        )
        cls.route = cls.warehouse.consu_route_id

        cls.project = cls.env["project.project"].create(
            {
                "name": "Job 123",
                "warehouse_id": cls.warehouse.id,
                "company_id": cls.company.id,
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Task 450",
                "project_id": cls.project.id,
                "company_id": cls.company.id,
                "date_planned": datetime.now(),
            }
        )

        cls.task_2 = cls.env["project.task"].create(
            {
                "name": "Task 452",
                "project_id": cls.project.id,
                "company_id": cls.company.id,
                "date_planned": datetime.now(),
            }
        )

        cls.vendor = cls.env["res.partner"].create({"name": "Partner A"})

        cls.product_category = cls.env["product.category"].create(
            {
                "name": "Category 1",
                "property_valuation": "manual_periodic",
                "property_cost_method": "standard",
            }
        )

        cls.product_a_value = 50
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "Product A",
                "default_code": "PROD_A",
                "type": "product",
                "categ_id": cls.product_category.id,
                "standard_price": cls.product_a_value,
                "seller_ids": [(0, 0, {"name": cls.vendor.id})],
                "route_ids": [
                    (4, cls.env.ref("purchase_stock.route_warehouse0_buy").id)
                ],
            }
        )
        cls.env["product.supplierinfo"].create(
            {
                "name": cls.vendor.id,
                "product_tmpl_id": cls.product_a.product_tmpl_id.id,
                "delay": 2,
            }
        )
        cls.product_b_value = 100
        cls.product_b = cls.env["product.product"].create(
            {
                "name": "Product B",
                "default_code": "PROD_B",
                "type": "product",
                "categ_id": cls.product_category.id,
                "standard_price": cls.product_b_value,
                "seller_ids": [(0, 0, {"name": cls.vendor.id})],
                "route_ids": [
                    (4, cls.env.ref("purchase_stock.route_warehouse0_buy").id)
                ],
            }
        )

    @classmethod
    def _create_material_line(cls, task=None, product=None, initial_qty=1):
        """Create a new material line.

        Use project user to create the line to verify that no access error is raised.
        Return the material lines with sudo priviledges for assertions.
        """
        new_line = (
            cls.env["project.task.material"]
            .with_user(cls.project_user)
            .create(
                {
                    "task_id": task.id if task else cls.task.id,
                    "product_id": product.id if product else cls.product_a.id,
                }
            )
        )
        new_line.initial_qty = initial_qty

        new_line.refresh()
        return new_line.sudo()

    @classmethod
    def _force_transfer_move(cls, move, quantity=None):
        """Force the transfer of a stock move.

        Use stock user to transfer the move to verify that no access error is raised.
        """
        move.move_line_ids |= (
            cls.env["stock.move.line"]
            .with_user(cls.stock_user)
            .create(
                dict(
                    move._prepare_move_line_vals(),
                    qty_done=quantity or move.product_uom_qty,
                )
            )
        )
        move.picking_id._action_done()

    @classmethod
    def _return_stock_move(cls, move_to_return, returned_qty):
        """Return the given stock move.

        Use stock user to transfer the move to verify that no access error is raised.
        Return the stock moves with sudo priviledges for assertions.

        :param move_to_return: the stock move to return
        :param returned_qty: the quantity to return
        """

        return_form = Form(
            cls.env["stock.return.picking"]
            .with_user(cls.stock_user)
            .with_context(
                active_id=move_to_return.picking_id.id, active_model="stock.picking"
            )
        )

        wizard = return_form.save()

        for product_return in wizard.product_return_moves:
            if product_return.move_id == move_to_return:
                product_return.quantity = returned_qty

        return_picking_id, pick_type_id = wizard._create_returns()
        return_picking = (
            cls.env["stock.picking"].with_user(cls.stock_user).browse(return_picking_id)
        )
        cls._force_transfer_move(return_picking.move_lines)
        return return_picking.move_lines.sudo()
