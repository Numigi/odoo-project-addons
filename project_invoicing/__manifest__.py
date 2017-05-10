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
        'employee_product',
        'hr_timesheet_sheet',
        'project',
        'sale_stock',
        'web',
    ],
    'data': [
        'views/project_project.xml',
        'views/project_config_settings.xml',
        'views/account_invoice.xml',
    ],
    'demo': [
        'demo/product_product.xml',
        'demo/hr_employee.xml',
        'demo/res_users.xml',
        'demo/project_project.xml',
        'demo/project_task.xml',
        'demo/timesheet_account_analytic_line.xml',
    ],
    'qweb': [
        'static/src/xml/project_widget.xml',
    ],
    'installable': True,
    'application': True,
}
