# Copyright 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    task_id = fields.Many2one("project.task", "Task")
    project_id = fields.Many2one(
        related="task_id.project_id",
        store=True,
        readonly=True,
    )
