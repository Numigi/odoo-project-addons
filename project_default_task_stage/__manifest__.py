# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Default Task Stages',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Default task stages on projects.',
    'depends': [
        'project_type',
        'project_stage_no_quick_create',
    ],
    'data': [
        'views/project_type.xml',
    ],
    'installable': True,
}
