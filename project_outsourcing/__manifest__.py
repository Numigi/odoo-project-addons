# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Outsourcing",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Generate outsourcing purchase orders from tasks",
    "depends": ["purchase_stock", "project_task_analytic_lines",
                "sale_management"],
    "data": [
        "views/account_invoice.xml",
        "views/project_project.xml",
        "views/project_task.xml",
        "views/purchase_order.xml",
        "views/purchase_order_line.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
