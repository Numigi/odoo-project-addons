# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Analytic Lines',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add a task on journal entries and vendor bills',
    'depends': [
        'sale_management',
        'account',
        'hr_timesheet',
    ],
    'data': [
        'views/account_analytic_line.xml',
        'views/account_invoice.xml',
        'views/account_move_line.xml',
    ],
    'installable': True,
}
