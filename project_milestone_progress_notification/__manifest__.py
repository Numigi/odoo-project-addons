# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Milestone Progress Notification",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "project",
    "depends": [
        "project_milestone",
    ],
    "summary": "Sends email notification when reaching project milestone progression.",
    "data": [
        "views/res_config_settings_views.xml",
        "data/cron_data.xml",
        "data/mail_template_data.xml",
        "data/res_config_settings_data.xml",
    ],
    "installable": True,
}
