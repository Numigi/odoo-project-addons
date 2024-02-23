# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectSteeringKpi(models.Model):
    _name = "project.steering.kpi"
    _description = "Project Steering KPI"
    _order = "sequence, id"

    name = fields.Char(string="Label", translate=True)
    sequence = fields.Integer(string="Sequence")
    model = fields.Char(required=True, related="model_id.model", string="Model Name")
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        domain=lambda self: self._get_allowed_model(),
        index=True,
        ondelete="set null",
    )
    active = fields.Boolean(default=True)
    filter_domain = fields.Char(string="Filter")

    def _get_allowed_model(self):
        return [("model", "in", ("project.task", "project.project"))]
