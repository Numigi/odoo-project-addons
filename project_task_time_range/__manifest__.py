# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Time Range',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add fields Min and Max on project tasks.',
    'depends': ['hr_timesheet'],
    'data': [
        'views/portal.xml',
        'views/project_task.xml',
    ],
    'installable': True,
}
