# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    duration = fields.Float(
        string="Duration",
        help="Indicates the duration of the milestone in calendar weeks (7 days)",
    )
    target_date = fields.Date(
        string="End Date",
        readonly=True,
    )

    @api.onchange("start_date", "duration")
    def onchange_date_start_duration(self):
        for record in self:
            if record.start_date and record.duration:
                record.target_date = record.start_date + \
                                     relativedelta(weeks=record.duration)
            else:
                record.target_date = False
