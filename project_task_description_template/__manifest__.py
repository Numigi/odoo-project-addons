# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Description Template",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Autocomplete task descriptions from templates",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
        "views/task_description_template_views.xml",
    ],
    "installable": True,
}
