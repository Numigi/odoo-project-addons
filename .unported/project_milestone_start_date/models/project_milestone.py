# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    start_date = fields.Date(string="Start Date")
