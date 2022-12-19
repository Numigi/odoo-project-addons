# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountAnalytic_line(models.Model):

    _inherit = "account.analytic.line"

    milestone_id = fields.Many2one(
        "project.milestone",
        related="task_id.milestone_id",
        string="Milestone",
        index=True,
        compute_sudo=True,
        store=True,
    )
