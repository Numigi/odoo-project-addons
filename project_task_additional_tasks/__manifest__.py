# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Additional Tasks",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "project",
    "depends": [
        "project",
    ],
    "summary": """
        Distinguish additional costs from the initial quote in order to potentially
        be able to re-invoice these new costs to the client.
    """,
    "data": [
        "views/project_task_views.xml",
    ],
    "installable": True,
}
