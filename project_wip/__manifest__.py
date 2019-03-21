# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Work In Progress',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Manage Work In Progress Accounting',
    'depends': [
        'account',
        'project',
        'project_type',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_no_analytic.xml',
        'views/project_type.xml',
        'views/project_wip_to_cgs.xml',
    ],
    'installable': True,
}
