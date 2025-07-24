# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Stages',
    'version': "1.0.2",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add stages on projects.',
    'depends': ['project'],
    'data': [
        'views/project.xml',
        'views/project_stage.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
