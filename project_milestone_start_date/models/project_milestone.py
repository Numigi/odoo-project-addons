# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    start_date = fields.Date(string="Start Date")

    @api.constrains("start_date", "target_date")
    def _check_date_start_before_date_end(self):
        if self.start_date > self.target_date:
            raise ValidationError(_('The milestone start date must be before '
                                    'the milestone end date.'))
