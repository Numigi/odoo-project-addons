# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Report Milestone Time",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add a dynamic milestone time report on projects",
    "depends": [
        "project_iteration",
        "project_lump_sum",
        "project_milestone_time_kpi",
    ],
    "data": [
        "report/report.xml",
        "views/project_project_views.xml",
        "views/project_milestone_views.xml",
    ],
    "qweb": ["static/src/xml/templates.xml"],
    "installable": True,
}
