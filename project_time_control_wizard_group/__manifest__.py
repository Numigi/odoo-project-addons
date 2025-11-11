# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Time Control Wizard Group',
    'version': '14.0.1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Assign the timer wizard to internal user group',
    'depends': [
        'project_timesheet_time_control',
    ],
    'data': [
        "security/ir.model.access.csv",
    ],
    'installable': True,
}
