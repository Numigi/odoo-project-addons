# -*- coding: utf-8 -*-
# © 2017-2018 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

{
    'name': 'Project Stage No Quick Create',
    'version': '1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'licence': 'LGPL-3',
    'category': 'Project Management',
    'summary': 'Disable project stage quick create',
    'depends': ['project'],
    'data': [
        'views/project_project.xml',
        'views/project_task.xml',
        'views/project_task_type.xml',
    ],
    'installable': True,
}
