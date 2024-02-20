# © 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Task(models.Model):

    _inherit = 'project.task'

    material_line_ids = fields.One2many(
        domain=[('is_direct_consumption', '=', False)]
    )

    direct_material_line_ids = fields.One2many(
        'project.task.material',
        'task_id',
        'Material (Direct Consumption)',
        readonly=True,
        domain=[('is_direct_consumption', '=', True)]
    )
