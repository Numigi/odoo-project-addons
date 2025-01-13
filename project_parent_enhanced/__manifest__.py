# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Parent Enhanced",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": """
        Enhances the functionality of parent-child relationships
        between projects and tasks.""",
    "depends": ["project", "project_parent"],
    "data": [
        "views/project_project_views.xml",
        "views/project_task_views.xml",
    ],
    "installable": True,
}
