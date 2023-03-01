# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project Task Kanban Draggable Column Disable',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    "website": "https://bit.ly/numigi-com",
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Disable stage column drag and drop on task kanban view',
    'depends': [
        'project',
        'kanban_draggable',
    ],
    'data': [
        'views/project_task.xml',
    ],
    'installable': True,
}
