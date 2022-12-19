# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Type',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add a field for typing tasks.',
    'depends': ['project'],
    'data': [
        'views/project_task.xml',
        'views/task_type.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
