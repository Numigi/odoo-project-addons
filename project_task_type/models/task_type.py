# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TaskType(models.Model):

    # project.task.type is already used to designate a workflow stage for a task.
    _name = "task.type"
    _description = "Task Type"
    _order = "sequence"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer()
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string="Color Index")
