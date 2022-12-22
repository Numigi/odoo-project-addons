# -*- coding: utf-8 -*-
# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task ID In Display Name',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add the ID of a task to its displayed name.',
    'depends': ['project'],
    'data': [
        'views/project_task.xml',
    ],
    'installable': True,
    'post_init_hook': 'post_init_hook',
}
