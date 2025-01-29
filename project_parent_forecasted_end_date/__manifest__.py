# Copyright 2024 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Parent Forecasted End Date",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Automatically calculate the project Forecasted End Date from chis childs",
    "depends": [
        "project_parent",
        "project_parent_enhanced",
    ],
    "data": ["views/project_project_views.xml", "views/project_type_views.xml"],
    "installable": True,
}
