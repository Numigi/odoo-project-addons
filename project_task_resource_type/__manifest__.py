# -*- coding: utf-8 -*-
# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Task Resource Type",
    "version": "1.0.0",
    "category": "Build'r",
    "description": "Add the referentiel Resource and the field to the tasks.",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "www.numigi.com",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_resource_views.xml",
        "views/project_task_views.xml",
    ],
    "application": False,
    "license": "LGPL-3",
    "installable": True,
}
