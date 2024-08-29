# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Project(models.Model):

    _inherit = 'project.project'

    @api.depends('stage_id', 'stage_id.allow_timesheet')
    def _compute_allow_timesheet(self):
        for record in self:
            record.allow_timesheets = record.stage_id.allow_timesheet

    allow_timesheets = fields.Boolean(
        readonly=True, compute="_compute_allow_timesheet", store=True,
        help="Depends if the project stage allows timesheet."
    )
