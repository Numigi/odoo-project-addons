# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):

    _inherit = "project.task"

    @api.constrains("is_template")
    def _check_template_can_not_have_timesheets(self):
        templates = self.filtered(lambda t: t.is_template)
        for template in templates:
            timesheet_lines = template.timesheet_ids | template.mapped(
                "child_ids.timesheet_ids"
            )
            if timesheet_lines:
                raise ValidationError(
                    _(
                        "The task {} can not be a template "
                        "because it already has timesheet lines."
                    ).format(template.display_name)
                )
