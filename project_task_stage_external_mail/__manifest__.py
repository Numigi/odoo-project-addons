# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Stage External Mail',
    'version': '1.0.0',
    'category': 'Project',
    'summary': "Send an external email for a task stage",
    'author': 'Numigi',
    'depends': [
        'project',
        'mail',
    ],
    'data': [
        'views/project_task_type.xml',
    ],
    'demo': [
        'demo/mail_template.xml',
    ],
    'license': 'LGPL-3',
    'application': False,
}
