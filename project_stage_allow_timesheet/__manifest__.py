# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Stage Allow Timesheet',
    'summary': """
        Allows to tell that a project stage is opened for timesheets.""",
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'depends': [
        'hr_timesheet',
        'project_stage',
    ],
    'data': [
        'views/project_stage.xml',
    ],
}
