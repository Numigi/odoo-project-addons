# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Analytic Group",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add analytic groups on projects and tasks",
    "depends": ["hr_timesheet"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_project.xml",
        "views/project_task.xml",
    ],
    "installable": True,
}
