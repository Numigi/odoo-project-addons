# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Invoicing Profile",
    "version": "2.1.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add iterations to projects",
    "depends": ["project"],
    "data": [
        "security/groups.xml",
        "views/project_invoice_profile.xml",
        "views/project_project.xml",
        'security/ir.model.access.csv',

    ],
    "installable": True,
}
