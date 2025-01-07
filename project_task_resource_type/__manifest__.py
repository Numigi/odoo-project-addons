# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Resource Type",
    "version": "16.0.1.0.0",
    "description": "Add resource type to tasks",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_resource_views.xml",
        "views/project_task_views.xml",
    ],
    "application": False,
    "installable": True,
}
