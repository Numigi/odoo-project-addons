# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Automated Task Creation',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Project Management',
    'summary': 'Add rule-based creation of tasks from templates on any model.',
    'depends': [
        'base_action_rule',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task.xml',
        'views/project_task_rule.xml',
        'views/project_task_template.xml',
        'views/menu.xml',
        'wizards/project_task_rule_condition_wizard.xml',
    ],
    'installable': False,
    'application': False,
}
