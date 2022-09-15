# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Milestone Remaining Hours',
    'version': '1.0.0',
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    'summary': "This module allow to compute remaining hours of a project milestone",
    'depends': [
        'project_milestone_estimated_hours',
        'project_milestone_spent_hours'
    ],
    'data': [
          'views/project_milestone.xml',
          'views/project_project.xml',
    ],
    'installable': True,
}
