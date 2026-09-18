# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _


class ProjectWorksheetLine(models.Model):
    _name = "project.worksheet.line"
    _description = "Project Worksheet Line"

    worksheet_id = fields.Many2one(
        comodel_name="project.worksheet",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=True,
    )
    project_id = fields.Many2one(
        related="worksheet_id.project_id",
        store=True,
    )
    task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task",
        required=True,
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    unit_amount = fields.Float(
        string="Hours",
        required=True,
    )

    @api.constrains("date", "worksheet_id")
    def _check_date_in_worksheet_period(self):
        invalid_lines = (line for line in self if line._is_date_out_of_period())
        for _line in invalid_lines:
            self._raise_date_out_of_period_error()

    def _is_date_out_of_period(self):
        if not self.worksheet_id or not self.date:
            return False
        return (self.date < self.worksheet_id.date_start
                or self.date > self.worksheet_id.date_end)

    def _raise_date_out_of_period_error(self):
        raise ValidationError(
            _("The date of a worksheet line must fall within the worksheet period.")
        )
