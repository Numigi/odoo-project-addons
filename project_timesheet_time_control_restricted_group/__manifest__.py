# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Timesheet Time Control Restricted Group",
    "version": "1.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Launch Timers only from the kanban view of tasks",
    "depends": ["project_timesheet_time_control"],
    "data": [
        "security/project_timesheet_time_control_security.xml",
        "views/project_views.xml",
    ],
    "installable": True,
}
