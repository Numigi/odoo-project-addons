# © 2020 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Iteration Parent Type Required',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Allow to tag projet types to force to have project parent',
    'depends': [
        'project_iteration',
        'project_type',
        'base_view_inheritance_extension',
    ],
    'data': [
        'views/project_project_views.xml',
        'views/project_type_views.xml',
    ],
    'installable': True,
}
