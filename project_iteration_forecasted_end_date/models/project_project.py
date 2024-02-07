# © 2024- today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    forecasted_end_date = fields.Date(
        string="Forecasted End Date",
        compute="_compute_forecasted_date",
        store=True,
    )

    @api.multi
    @api.depends(
        'child_ids', 'child_ids.active',
        'child_ids.date', 'child_ids.project_type_id',
        'child_ids.project_type_id.exclude_forecasted_end_date',
        )
    def _compute_forecasted_date(self):
        for project in self:
            if project.is_parent:
                project.forecasted_end_date = max(child.date for child in project.child_ids.filtered(
                    lambda c: c.active and c.date and not c.project_type_id.exclude_forecasted_end_date))
