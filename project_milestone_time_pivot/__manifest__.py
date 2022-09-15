# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Milestone Time Pivot',
    'version': '1.0.0',
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    'summary': "This module provide a pivot view in project's milestones",
    'depends': [
        'project_milestone_remaining_hours',
    ],
    'data': [
          'views/project_milestone.xml',
    ],
    'installable': True,
}
