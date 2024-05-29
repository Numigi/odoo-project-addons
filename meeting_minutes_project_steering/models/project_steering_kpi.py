# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


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
    primary_filter_domain = fields.Char(string="Primary Filter")
    date_filter_domain_id = fields.Many2one(
        "search.date.range.filter",
        string="Date Filter",
        domain="[('model_id', '=', model_id)]",
        store=True,
        help="Filter domain applied on the selected model and the primary filter.",
    )
    date_filter_domain = fields.Char(
        compute="_get_domain", string="Date Filter Domain", store=True
    )

    def _get_allowed_model(self):
        return [("model", "in", ("project.task", "project.project"))]

    @api.depends("date_filter_domain_id")
    def _get_domain(self):
        for record in self:
            record.date_filter_domain = record.date_filter_domain_id.domain


class SearchDateRangeFilter(models.Model):
    _inherit = "search.date.range.filter"

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = _("'%s' applied on '%s'") % (
                record.range_id.label,
                record.field_id.field_description,
            )

            result.append((record.id, name))
        return result
