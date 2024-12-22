# Copyriht 2023-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Outsourcing",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Generate outsourcing purchase orders from tasks",
    "depends": ["purchase_stock", "sale_management"],
    "data": [
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
