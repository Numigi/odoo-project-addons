# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Iteration',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add iterations to projects',
    'depends': [
        'hr_timesheet',
        'project',
    ],
    'data': [
        'views/account_analytic_line.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/search_input_many2many.xml',
    ],
    'installable': True,
}
