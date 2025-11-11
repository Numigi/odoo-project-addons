# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Analytic Lines',
    'version': '14.0.1.1.1',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add a task on journal entries and vendor bills',
    'depends': [
        'account',
        'hr_timesheet',
    ],
    'data': [
        'views/account_analytic_line.xml',
        'views/account_move_line.xml',
    ],
    'installable': True,
}
