# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Track End Date",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Project",
    "summary": """
    Gives the possibility to trace the changes in the end of validity date of each project/lot.
    """,
    "depends": ["project_stage", "project_timeline"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_project.xml",
        "wizard/edit_date_wizard_views.xml",
    ],
    "installable": True,
}