# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

{
    'name': 'Project Stage No Quick Create',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'licence': 'LGPL-3',
    'category': 'Project Management',
    'summary': 'Disable project quick stage creation',
    'depends': ['project'],
    'data': [
        'views/project_stage.xml',
        'views/project_project.xml',
        'views/project_task_type.xml',
        ],
    'installable': True,
    'application': False,
}
