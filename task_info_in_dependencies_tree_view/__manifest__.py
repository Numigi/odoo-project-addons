# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Task Info In Dependencies Tree View",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "project",
    "depends": [
        "project_task_dependency",
    ],
    "summary": "Shows the ID of each task listed in the dependencies as well as their kanban states",
    "data": [
        "views/project_task_view.xml",
    ],
    "installable": True,
}
