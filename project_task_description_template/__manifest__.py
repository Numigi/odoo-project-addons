# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Task Description Template",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Autocomplete task descriptions from templates",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task.xml",
        "views/project_task_description_template.xml",
    ],
    "installable": True,
}
