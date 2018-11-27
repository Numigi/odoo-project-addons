# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Time Management',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add fields Min and Max on project.',
    'depends': [
        'project_time_range',
        'project_task_time_range',
        'project_accurate_time_spent',
    ],
    'data': [
        'views/project_project.xml',
    ],
    'installable': True,
}
