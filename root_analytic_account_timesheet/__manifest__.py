# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Root Account Analytic Timesheet",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Project",
    "summary": "Add root analytic account on account analytic line",
    "depends": ["hr_timesheet", "account_analytic_root"],
    "data": [
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
}
