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
    'summary': 'Add a new field forecasted end date in the project. This field take as'
               ' value the largest date among the end dates of the project iterations',
    'depends': [
                'project_iteration',
                'project_milestone_time_kpi',
                'project_type',
    ],
    'data': [
        'views/project_view.xml',
    ],
    'installable': True,
}
