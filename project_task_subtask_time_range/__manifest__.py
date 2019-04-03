# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Subtask Time Range',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Add computed fields that sum time details from subtasks.',
    'depends': [
        'hr_timesheet',
        'project_task_time_range'
    ],
    'data': [
        'views/project_task.xml',
    ],
    'installable': True,
}
