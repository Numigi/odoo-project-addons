# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class ProjectCostReportCase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Job 123"})

        cls.analytic_account = cls.project.analytic_account_id

        cls.product_group_a = cls.env["project.cost.category"].create(
            {"name": "Product Group A", "sequence": 1, "target_margin": 36}
        )
        cls.product_group_b = cls.env["project.cost.category"].create(
            {"name": "Product Group B", "sequence": 2, "target_margin": 50}
        )

        cls.category_a = cls.env["product.category"].create(
            {"name": "Category A", "project_cost_category_id": cls.product_group_a.id}
        )
        cls.category_b = cls.env["product.category"].create(
            {"name": "Category B", "project_cost_category_id": cls.product_group_b.id}
        )

        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "type": "product", "categ_id": cls.category_a.id}
        )

        cls.product_b = cls.env["product.product"].create(
            {"name": "Product B", "type": "product", "categ_id": cls.category_b.id}
        )

        cls.service_a = cls.env["product.product"].create(
            {"name": "Service A", "type": "service", "categ_id": cls.category_a.id}
        )

        cls.product_line_1 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Line 1",
                "product_id": cls.product_a.id,
                "unit_amount": 1,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": -100,
            }
        )

        cls.product_line_2 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Line 2",
                "product_id": cls.product_b.id,
                "unit_amount": 2,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": -200,
            }
        )

        cls.product_line_3 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Line 3",
                "product_id": cls.product_b.id,
                "unit_amount": 3,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": -300,
            }
        )

        cls.time_group_labour = cls.env.ref("project_cost_report.cost_category_labour")
        cls.time_group_labour.target_hourly_rate = 100
        cls.time_group_1 = cls.env["project.cost.category"].create(
            {"name": "Time Group 1", "sequence": 1, "target_hourly_rate": 200}
        )
        cls.time_group_2 = cls.env["project.cost.category"].create(
            {"name": "Time Group 2", "sequence": 2, "target_hourly_rate": 300}
        )
        cls.task_type_1 = cls.env["task.type"].create(
            {"name": "Type 1", "project_cost_category_id": cls.time_group_1.id}
        )
        cls.task_type_2 = cls.env["task.type"].create(
            {"name": "Type 2", "project_cost_category_id": cls.time_group_2.id}
        )

        cls.task_1 = cls.env["project.task"].create(
            {"name": "Task 1", "project_id": cls.project.id}
        )

        cls.task_2 = cls.env["project.task"].create(
            {
                "name": "Task 2",
                "project_id": cls.project.id,
                "task_type_id": cls.task_type_1.id,
            }
        )

        cls.task_3 = cls.env["project.task"].create(
            {
                "name": "Task 3",
                "project_id": cls.project.id,
                "task_type_id": cls.task_type_2.id,
            }
        )

        cls.env.user.employee_ids.write({"timesheet_cost": 100})

        cls.time_line_1 = cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project.id,
                "name": "Time 1",
                "product_uom_id": cls.env.ref("uom.product_uom_hour").id,
                "unit_amount": 4,
                "amount": -400,
                "user_id": cls.env.user.id,
                "task_id": cls.task_1.id,
            }
        )
        cls.time_line_1.amount = -400

        cls.time_line_2 = cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project.id,
                "name": "Time 2",
                "product_uom_id": cls.env.ref("uom.product_uom_hour").id,
                "unit_amount": 5,
                "amount": -500,
                "user_id": cls.env.user.id,
                "task_id": cls.task_2.id,
            }
        )
        cls.time_line_2.amount = -500

        cls.time_line_3 = cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project.id,
                "name": "Time 3",
                "product_uom_id": cls.env.ref("uom.product_uom_hour").id,
                "unit_amount": 6,
                "amount": -600,
                "user_id": cls.env.user.id,
                "task_id": cls.task_2.id,
            }
        )
        cls.time_line_3.amount = -600

        cls.time_line_4 = cls.env["account.analytic.line"].create(
            {
                "project_id": cls.project.id,
                "name": "Time 3",
                "product_uom_id": cls.env.ref("uom.product_uom_hour").id,
                "unit_amount": 7,
                "amount": -700,
                "user_id": cls.env.user.id,
                "task_id": cls.task_3.id,
            }
        )
        cls.time_line_4.amount = -700

        cls.outsourcing_group = cls.env.ref(
            "project_cost_report.cost_category_outsourcing"
        )
        cls.outsourcing_group.target_margin = 20

        cls.outsourcing_line_1 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Service Line 1",
                "product_id": cls.service_a.id,
                "unit_amount": 1,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": -800,
            }
        )

        cls.outsourcing_line_2 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Service Line 2",
                "product_id": cls.service_a.id,
                "unit_amount": 2,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": -900,
            }
        )

        # Add revenue analytic lines
        # These amounts must be excluded from cost categories
        # (Outsourcing, Products, Time)
        cls.revenue_line_1 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Revenue Line 1",
                "product_id": cls.service_a.id,
                "unit_amount": 1,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": 100,
                "revenue": True,
            }
        )

        cls.revenue_line_2 = cls.env["account.analytic.line"].create(
            {
                "account_id": cls.analytic_account.id,
                "name": "Revenue Line 2",
                "product_id": cls.product_a.id,
                "unit_amount": 1,
                "product_uom_id": cls.env.ref("uom.product_uom_unit").id,
                "amount": 200,
                "revenue": True,
            }
        )

        cls.report = cls.env["project.cost.report"].create({})
