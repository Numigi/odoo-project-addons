# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectWorksheetLine(models.Model):
    _name = "project.worksheet.line"
    _description = "Project Worksheet Line"
    _order = "sequence, date, id"

    sequence = fields.Integer(
        default=10,
    )
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
        required=False,
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
        return (
            self.date < self.worksheet_id.date_start
            or self.date > self.worksheet_id.date_end
        )

    def _raise_date_out_of_period_error(self):
        raise ValidationError(
            _("The date of a worksheet line must fall within the worksheet period.")
        )

    @api.constrains("date", "employee_id", "worksheet_id")
    def _check_timesheet_sheet_not_locked(self):
        for line in self:
            if line._has_locked_timesheet_sheet():
                line._raise_locked_timesheet_sheet_error()

    def _has_locked_timesheet_sheet(self):
        if not self.employee_id or not self.date:
            return False
        domain = self._get_locked_timesheet_sheet_domain()
        return bool(self.env["hr_timesheet.sheet"].sudo().search_count(domain))

    def _get_locked_timesheet_sheet_domain(self):
        company = self.worksheet_id.company_id or self.env.company
        return [
            ("employee_id", "=", self.employee_id.id),
            ("company_id", "=", company.id),
            ("date_start", "<=", self.date),
            ("date_end", ">=", self.date),
            ("state", "in", ("confirm", "done")),
        ]

    def _raise_locked_timesheet_sheet_error(self):
        raise ValidationError(
            _(
                "You cannot add or modify hours for employee %(employee)s on "
                "%(date)s because their timesheet sheet for this period is "
                "already confirmed or approved."
            )
            % {
                "employee": self.employee_id.name,
                "date": self.date,
            }
        )
