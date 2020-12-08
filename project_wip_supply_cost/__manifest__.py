# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project WIP Supply Cost',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Generate indirect cost entries from timesheets',
    'depends': [
        'project_wip',
        'project_task_analytic_lines',
        'hr_timesheet',
    ],
    'data': [
        'views/project_type.xml',
    ],
    'installable': True,
}
