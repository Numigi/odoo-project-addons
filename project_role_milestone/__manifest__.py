# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Role Milestone',
    'version': '1.0.0',
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    'summary': 'Manage role for a project milestone',
    'depends': [
        'project_role',
        'project_milestone'
    ],
    'data': [
          'security/ir.model.access.csv',
          'views/project_assignment.xml',
          'views/project_milestone.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
