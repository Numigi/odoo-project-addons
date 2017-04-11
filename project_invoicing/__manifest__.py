# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

{
    'name': 'Project Invoicing',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'https://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Prepare Invoices from Projects',
    'depends': [
        'account',
        'analytic_line_is_timesheet',
        'hr_timesheet_sheet',
        'project',
        'sale_stock',
        'web',
    ],
    'data': [
        'views/project_project.xml',
    ],
    'qweb': [
        'static/src/xml/project_invoicing.xml',
    ],
    'installable': True,
    'application': True,
}
