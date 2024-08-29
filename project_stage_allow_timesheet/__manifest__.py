# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Stage Allow Timesheet",
    "summary": """
        Allows to tell that a project stage is opened for timesheets.""",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "depends": ["hr_timesheet"],
    "data": [
        "views/res_config_settings.xml",
        "views/project_stage_views.xml",
        "views/project_task_type_views.xml",
    ],
}
