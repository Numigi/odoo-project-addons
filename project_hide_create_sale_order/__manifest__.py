# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Hide Create Sale Order',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Hide the button Create Sale Order on project',
    'depends': [
        'sale_timesheet',
    ],
    'data': [
        'views/project.xml',
    ],
    'installable': True,
}
