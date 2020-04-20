# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):

    _inherit = "project.project"

    analytic_group_id = fields.Many2one(
        related="analytic_account_id.group_id",
        store=True,
        index=True,
        string="Analytic Group",
    )
