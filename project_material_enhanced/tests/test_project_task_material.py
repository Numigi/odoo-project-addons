# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProjectTaskMaterial(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.picking_model = cls.env["stock.picking"]
        cls.product_model = cls.env["product.product"]
        cls.template_model = cls.env["product.template"]
        cls.attribute_model = cls.env["product.attribute"]
        cls.attribute_value_model = cls.env["product.attribute.value"]

        cls.supplier_location = cls.env.ref("stock.stock_location_suppliers")
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.main_company = cls.env.ref("base.main_company")

        cls.location_bin_a = cls.env["stock.location"].create(
            {
                "usage": "internal",
                "name": "Location Bin A",
                "location_id": cls.stock_location.id,
                "company_id": cls.main_company.id,
            }
        )

        cls.location_bin_b = cls.env["stock.location"].create(
            {
                "usage": "internal",
                "name": "Location Bin B",
                "location_id": cls.stock_location.id,
                "company_id": cls.main_company.id,
            }
        )

        cls.env["stock.location"]._parent_store_compute()

        cls.template_product = cls.template_model.create(
            {"name": "Template Product", "uom_id": cls.uom_unit.id, "type": "product"}
        )

        # Create product attributes and values
        cls.attribute_color = cls.attribute_model.create(
            {"name": "Color", "sequence": 1}
        )
        cls.attribute_value_white = cls.attribute_value_model.create(
            {"name": "White", "attribute_id": cls.attribute_color.id, "sequence": 2}
        )

        cls.product_attribute_line = cls.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": cls.template_product.id,
                "attribute_id": cls.attribute_color.id,
                "value_ids": [
                    (
                        6,
                        0,
                        [
                            cls.attribute_value_white.id,
                        ],
                    )
                ],
            }
        )
        cls.product_variant_a = cls.template_product.product_variant_ids[0]

        cls.env["stock.quant"].create(
            {
                "product_id": cls.product_variant_a.id,
                "location_id": cls.stock_location.id,
                "quantity": 7,
            }
        )

    def test_product_availability(self):
        """Test the available quantity computation for products."""
        task = self.env["project.task"].create(
            {
                "name": "Test Task",
                "project_id": self.env.ref("project.project_project_1").id,
                "date_planned": "2024-01-01",
            }
        )
        material = self.env["project.task.material"].create(
            {
                "product_id": self.product_variant_a.id,
                "task_id": task.id,
            }
        )

        self.assertEqual(
            material.available_qty,
            7,
            "Available quantity should be 7 for product_variant_a",
        )

        picking = self.picking_model.create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "move_lines": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Move Out A",
                            "product_id": self.product_variant_a.id,
                            "product_uom": self.product_variant_a.uom_id.id,
                            "product_uom_qty": 2,
                            "location_id": self.stock_location.id,
                            "location_dest_id": self.customer_location.id,
                        },
                    )
                ],
            }
        )

        picking.action_confirm()
        picking.move_lines.quantity_done = 2
        picking.button_validate()

        material.refresh()

        self.assertEqual(
            material.available_qty,
            5,
            "Available quantity should be 5 for product_variant_a",
        )
