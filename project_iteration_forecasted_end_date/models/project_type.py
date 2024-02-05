# © 2024- today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectType(models.Model):

    _inherit = "project.type"

    exclude_forecasted_end_date = fields.Boolean(
        "Exclude From Forecasted End Date Computation")



