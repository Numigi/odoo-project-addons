# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Estimation",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Add an estimation mode on projects",
    "depends": ["project", "project_task_date_planned"],
    "data": [
        "wizard/project_estimation_enter.xml",
        "wizard/project_estimation_exit.xml",
        "views/project.xml",
        "views/project_task.xml",
    ],
    "installable": True,
}
