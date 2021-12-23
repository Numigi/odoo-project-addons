# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):

    _inherit = "project.project"

    estimation_mode_active = fields.Boolean(
        readonly=True,
        copy=False,
        default=lambda self: self._get_default_estimation_mode_active(),
        track_visibility="onchange",
    )

    def _get_default_estimation_mode_active(self):
        value = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("project_estimation_mode_active_default", "False")
        )
        return value.lower() == "true"
