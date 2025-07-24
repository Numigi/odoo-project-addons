# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Template',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Define templates for projects and tasks',
    'depends': [
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project.xml',
        'views/project_task.xml',
        'views/assets.xml',
        'wizard/project_task_template_add.xml',
    ],
    'installable': True,
}
