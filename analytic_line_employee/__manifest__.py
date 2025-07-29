# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Analytic Line Employee',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
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
