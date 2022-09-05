# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectMilestoneType(models.Model):
    _inherit = "project.milestone.type"

    html_color = fields.Char(
        string="HTML Color",
        default="#FFFFFF",
        help="You can define a specific HTML color index (e.g. #FF0000) that "
             "will be applied to Milestones of this Type in the Timeline view."
    )
