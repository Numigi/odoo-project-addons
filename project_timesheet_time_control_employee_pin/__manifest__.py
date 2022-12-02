# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Timesheet Time Control Employee PIN",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Enter times from the Timer of a task as a "
               "different employee from the logged in user",
    "depends": ["hr_attendance", "project_timesheet_time_control"],
    "data": [
        "views/account_analytic_line_views.xml",
        "wizards/hr_timesheet_switch_view.xml",
    ],
    "installable": True,
}
