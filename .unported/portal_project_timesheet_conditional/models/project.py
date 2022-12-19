# © 2022 today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Project(models.Model):

    _inherit = "project.project"

    timesheet_ids = fields.One2many("account.analytic.line", "project_id",
                                    string="Timesheets")
    total_hours_spent = fields.Float(
        string="Total spent hours",
        compute="_compute_total_hours_spent", store=True
    )

    @api.multi
    @api.depends("timesheet_ids", "timesheet_ids.project_id",
                 "timesheet_ids.unit_amount")
    def _compute_total_hours_spent(self):
        for project in self:
            project.total_hours_spent = \
                sum(project.timesheet_ids.mapped("unit_amount"))
