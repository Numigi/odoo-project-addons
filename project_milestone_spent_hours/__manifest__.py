# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Milestone Spent Hours",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": """Add field Total Hours in milestones which display the sum
                  of all hours of tasks associated to the milestone""",
    "depends": ["hr_timesheet", "project_milestone_enhanced"],
    "data": [
        "views/project_milestone.xml",
        "views/project.xml",
    ],
    "installable": True,
}
