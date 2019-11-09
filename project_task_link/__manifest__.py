# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Link',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Dynamically add links to tasks in the web interface.',
    'depends': [
        'project',

        # required because of the HTML editor field.
        'web_editor',
    ],
    'data': [
        'views/assets.xml',
    ],
    'installable': True,
}
