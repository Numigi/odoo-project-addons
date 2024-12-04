# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProjectSteeringKpi(models.Model):
    _inherit = "project.steering.kpi"

    def _get_allowed_model(self):
        res = super()._get_allowed_model()
        return [
            (
                field,
                operator,
                (
                    (value,) + ("project.project",)
                    if field == "model" and operator == "in"
                    else value
                ),
            )
            for field, operator, value in res
        ]
