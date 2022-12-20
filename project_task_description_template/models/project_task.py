# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    description_template_id = fields.Many2one(
        "project.task.description.template", ondelete="restrict"
    )

    @api.onchange("description_template_id")
    def _onchange_description_template(self):
        if self.description_template_id:
            self.description = self.description_template_id.description
