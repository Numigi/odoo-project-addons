# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Work In Progress",
    "version": "1.1.2",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Manage Work In Progress Accounting",
    "depends": ["account", "project", "hr_timesheet", "project_type"],
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
