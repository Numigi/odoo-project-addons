# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Time Management',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add calculated fields to project to have a view on hours of parent tasks.',
    'depends': [
        'project_time_range',
        'project_task_time_range',
    ],
    'data': [
        'views/project_project.xml',
    ],
    'installable': True,
}
