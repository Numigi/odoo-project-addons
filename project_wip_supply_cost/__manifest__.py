# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project WIP Supply Cost",
    "version": "14.0.0.1.0.2",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Generate indirect cost entries from timesheets",
    "depends": [
        "project_wip",
        "project_task_analytic_lines",
        "hr_timesheet",
    ],
    "data": [
        "views/project_type_views.xml",
    ],
    "installable": True,
}
