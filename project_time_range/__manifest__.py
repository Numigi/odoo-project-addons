# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Time Range",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add fields Min and Max on project tasks.",
    "depends": ["hr_timesheet"],
    "data": [
        "views/project_task_portal_template.xml",
        "views/project_task_views.xml",
        "views/project_project_views.xml",
    ],
    "installable": True,
}
