# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Milestone Time Progress",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": """Calculate progress of the milestone
     based on past and estimated hours.""",
    "depends": ["project_milestone_estimated_hours",
                "project_milestone_spent_hours"],
    "data": [
        "views/project_milestone.xml",
    ],
    "installable": True,
    "post_init_hook": "recompute_progress_hook",
    "uninstall_hook": "recompute_progress_hook",
}