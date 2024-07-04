# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Task Full Text Search",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "depends": ["project"],
    "external_dependencies": {
        "python": ["unidecode"],
    },
    "data": [
        "views/project_task.xml",
    ],
    "installable": True,
}
