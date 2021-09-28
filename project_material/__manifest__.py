# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Material",
    "version": "1.2.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Consume material on projects",
    "depends": ["project_task_date_planned", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/assets.xml",
        "views/project_project.xml",
        "views/project_task_material.xml",
        "views/project_task.xml",
        "views/stock_move.xml",
        "views/stock_move_line.xml",
        "views/stock_picking.xml",
        "views/stock_picking_type.xml",
        "views/stock_warehouse.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
