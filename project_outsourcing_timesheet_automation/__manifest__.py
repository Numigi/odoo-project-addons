# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Outsourcing Timesheet Automation",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Automate Outsourcing Timesheet",
    "depends": ["project_outsourcing",
                "hr_timesheet",
                "project_timesheet_time_control"],
    "data": [
        "views/product_views.xml",
        "views/res_partner_views.xml",
        "views/project_task_type_views.xml",
    ],
    "installable": True,
}
