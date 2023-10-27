# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TaskType(models.Model):

    _inherit = "task.type"

    project_cost_category_id = fields.Many2one(
        "project.cost.category", "Cost Report Category", ondelete="restrict"
    )
