# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Task Milestone Mandatory",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "In task form view, field milestone is required if field Use milestones is True in project else invisible",
    "depends": ["project_milestone_enhanced"],
    'data': [
        'views/project_task.xml',
    ],
    "installable": True,
}
