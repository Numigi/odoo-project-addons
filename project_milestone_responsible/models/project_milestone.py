# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, fields, api


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    user_id = fields.Many2one(
        "res.users",
        "Responsible",
        domain= [('share', '=', False)],
        help="Assign a responsible by choosing an Internal user"
    )

    @api.onchange("project_id")
    def _onchange_project_id(self):
        if self.project_id:
            self.user_id = self.project_id.user_id.id
