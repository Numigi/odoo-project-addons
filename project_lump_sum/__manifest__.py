# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Lump Sum",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Categorize projects as Lump Sum",
    "depends": ["project_category",
                "project_task_analytic_lines",
                "hr_timesheet"],
    "data": [
        "views/account_analytic_line.xml",
        "views/project.xml",
        "views/project_type.xml",
    ],
    "installable": True,
}
