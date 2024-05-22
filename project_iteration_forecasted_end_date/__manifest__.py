# © 2024 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Iteration Forecasted End Date',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Automatically calculate the project Forecasted End Date from Iterations',
    'depends': [
                'project_iteration',
                'project_type',
                'project_form_with_dates',
    ],
    'data': [
        'views/project_view.xml',
    ],
    'installable': True,
}
