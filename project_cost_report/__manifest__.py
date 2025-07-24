# Copyright 2019-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Cost Report",
    "version": "14.0.1.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add a dynamic cost report to projects",
    "depends": [
        "analytic_line_revenue",
        "project_task_analytic_lines",
        "project_task_type",
        "project_type",
        "purchase",
    ],
    "data": [
        "data/project_cost_category.xml",
        "report/report.xml",
        "security/ir.model.access.csv",
        "views/project_project_views.xml",
        "views/assets.xml",
        "views/project_cost_category_views.xml",
        "views/product_category_views.xml",
        "views/task_type_views.xml",
    ],
    "qweb": ["static/src/xml/templates.xml"],
    "installable": True,
}