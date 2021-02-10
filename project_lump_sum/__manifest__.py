# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Lump Sum",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Categorize projects as Lump Sum",
    "depends": ["project_type", "project_task_analytic_lines", "hr_timesheet"],
    "data": [
        "views/account_analytic_line.xml",
        "views/project.xml",
        "views/project_type.xml",
    ],
    "installable": True,
}
