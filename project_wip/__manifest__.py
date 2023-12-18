# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Work In Progress",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Manage Work In Progress Accounting",
    "depends": ["account", "stock", "project", "project_type", "account_reconciliation_widget"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "wizard/project_wip_transfer.xml",
        "views/account_move.xml",
        "views/project_project.xml",
        "views/project_type.xml",
    ],
    "installable": True,
}
