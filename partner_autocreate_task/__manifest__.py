# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Transport Partner Autocreate Task',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Sales Management',
    'summary': 'Autocreate tasks for Partners.',
    'depends': [
        'base',
        'project',
        'project_task_autocreate',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/task_autocreate.xml',
        'views/res_partner.xml',
        'data/ir_cron.xml',
    ],
    'installable': False,
    'application': False,
}
