# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Kanban Sequence Fixed',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    "website": "https://www.numigi.com",
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Lock the stage column drag and drop on kanban view of project task',
    'depends': [
        'project',
        'kanban_draggable',
    ],
    'data': [
        'views/project_task.xml',
    ],
    'installable': True,
}
