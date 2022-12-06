# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Manager Access Right",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": """Add advanced access right for project managers""",
    "depends": [
        "project_role",
        "project_milestone",
        "sale_timesheet",
    ],
    "data": [
        "security/project_security.xml",
        "security/ir.model.access.csv",
        "views/project_role_view.xml",
        "views/project_views.xml",
    ],
    "installable": True,
}
