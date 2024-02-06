# © 2024- today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    forecasted_end_date = fields.Date(
        string="Forecasted End Date",
        compute="_compute_forecasted_end_date",
        store=True,
    )
    remaining_days = fields.Float(
        string="Remaining weeks",
        compute="_compute_forecasted_end_date",
        store=True,
    )
    def _get_child_ids_end_date(self, child_ids):
        dates = []
        for rec in child_ids:
            if not rec.active:
                continue
            if rec.project_type_id.exclude_forecasted_end_date:
                continue
            if rec.date:
                dates.append(rec.date)
        return dates

    @api.multi
    @api.depends(
        'child_ids.date', 'child_ids.project_type_id.exclude_forecasted_end_date',
        'child_ids.active')
    def _compute_forecasted_end_date(self):
        for project in self:
            if project.child_ids:
                dates = self._get_child_ids_end_date(project.child_ids)
                if dates:
                    project.forecasted_end_date = max(dates)
                    dt = project.forecasted_end_date - fields.Date.today()
                    project.remaining_days = dt.days/7











