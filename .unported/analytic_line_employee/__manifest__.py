# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Analytic Line Employee',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add the employee to the views of analytic lines.',
    'depends': [
        'hr_timesheet',
    ],
    'data': [
        'views/account_analytic_line.xml',
    ],
    'installable': True,
}
