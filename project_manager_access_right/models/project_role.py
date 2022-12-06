# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectRole(models.Model):
    _inherit = "project.role"

    is_manager = fields.Boolean(
        "Is Manager",
        help="Check this box to identify the roles that the "
             "(Projects / Manager: Own Projects Only) rights group "
             "is based on. \n \n When a user belonging to this group is"
             " assigned to a project with this role, he can modify"
             " the project and see all of its data and indicators."
    )
