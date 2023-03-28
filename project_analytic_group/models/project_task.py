# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Task(models.Model):

    _inherit = "project.task"

    analytic_account_id = fields.Many2one(
        related="project_id.analytic_account_id", store=True, index=True
    )

    analytic_group_id = fields.Many2one(
        related="analytic_account_id.group_id",
        store=True,
        index=True,
        string="Analytic Group",
    )
