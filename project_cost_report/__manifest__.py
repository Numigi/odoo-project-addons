# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Cost Report',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add a dynamic cost report to projects',
    'depends': [
        'analytic_line_revenue',
        'project_task_analytic_lines',
        'project_task_type',
        'project_type',
        'purchase',
    ],
    'data': [
        'report.xml',
        'project.xml',
    ],
    'qweb': [
        'static/src/xml/templates.xml',
    ],
    'installable': True,
}
