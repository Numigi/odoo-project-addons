# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Project Remaining Hours Update",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Update the remaining hours on tasks",
    "depends": ["hr_timesheet"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_views.xml",
        "views/project_task_remaining_hours_views.xml",
        "views/project_task_type_views.xml",
        "wizard/project_task_remaining_hours_update.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
