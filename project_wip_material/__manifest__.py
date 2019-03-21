# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Project WIP Material',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Project',
    'summary': 'Consume material on projects',
    'depends': [
        'project_task_date_planned',
        'project_wip',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_with_warehouse.xml',
        'views/stock_picking_with_task.xml',
        'views/task_picking_smart_button.xml',
        'views/task_material_tab.xml',
        'views/warehouse.xml',
    ],
    'post_init_hook': '_update_warehouses_consumption_routes',
    'installable': True,
}
