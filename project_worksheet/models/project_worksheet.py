# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ProjectWorksheet(models.Model):
    _name = "project.worksheet"
    _description = "Project Worksheet"
    _inherit = ["portal.mixin", "mail.thread", "mail.activity.mixin"]
    _order = "date_start desc, id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        readonly=True,
        default=lambda self: self._default_name(),
        copy=False,
    )
    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Project",
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Client",
        related="project_id.partner_id",
        store=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    supervisor_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Supervisor",
        required=True,
        tracking=True,
    )
    date_start = fields.Date(
        string="Period Start",
        required=True,
        tracking=True,
    )
    date_end = fields.Date(
        string="Period End",
        required=True,
        tracking=True,
    )
    partner_approver_id = fields.Many2one(
        comodel_name="res.partner",
        string="Client Approver",
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("open", "Open"),
            ("pending", "Pending Approval"),
            ("confirmed", "Confirmed"),
        ],
        string="Status",
        default="new",
        tracking=True,
    )
    line_ids = fields.One2many(
        comodel_name="project.worksheet.line",
        inverse_name="worksheet_id",
        string="Worksheet Lines",
    )
    timesheet_ids = fields.One2many(
        comodel_name="account.analytic.line",
        inverse_name="worksheet_id",
        string="Generated Timesheets",
        readonly=True,
    )
    total_hours = fields.Float(
        string="Total Hours",
        compute="_compute_total_hours",
        store=True,
    )

    @api.depends("line_ids.unit_amount")
    def _compute_total_hours(self):
        for worksheet in self:
            worksheet.total_hours = sum(worksheet.line_ids.mapped("unit_amount"))

    def action_open(self):
        self.ensure_one()
        self.write({"state": "open"})

    def action_send_to_client(self):
        self.ensure_one()
        self._portal_ensure_token()
        self._send_approval_email()
        self.write({"state": "pending"})

    def action_manager_confirm(self):
        self.ensure_one()
        self._check_manager_approval_delay()
        self._confirm_worksheet()

    def action_client_confirm(self):
        self.ensure_one()
        self._confirm_worksheet()

    def _default_name(self):
        return self.env["ir.sequence"].next_by_code("project.worksheet") or _("New")

    def _compute_access_url(self):
        super()._compute_access_url()
        for worksheet in self:
            worksheet.access_url = "/my/worksheet/%s/%s" % (
                worksheet.id,
                worksheet.access_token,
            )

    def _send_approval_email(self):
        template = self.env.ref("project_worksheet.email_template_worksheet_approval")
        template.send_mail(self.id, force_send=True)

    def _check_manager_approval_delay(self):
        delay = self.company_id.worksheet_approval_delay
        allowed_date = self.create_date + timedelta(days=delay)
        if fields.Datetime.now() < allowed_date:
            self._raise_delay_error(delay)

    def _raise_delay_error(self, delay):
        raise UserError(
            _("You cannot approve this worksheet yet. A delay of %s days is required.") % delay
        )

    def _confirm_worksheet(self):
        self._generate_timesheets()
        self.write({"state": "confirmed"})

    def _generate_timesheets(self):
        timesheet_model = self.env["account.analytic.line"]
        for line in self.line_ids:
            self._create_single_timesheet(timesheet_model, line)

    def _create_single_timesheet(self, model, line):
        vals = self._prepare_timesheet_vals(line)
        model.create(vals)

    def _prepare_timesheet_vals(self, line):
        return {
            "worksheet_id": self.id,
            "date": line.date,
            "employee_id": line.employee_id.id,
            "project_id": self.project_id.id,
            "task_id": line.task_id.id,
            "name": line.name,
            "unit_amount": line.unit_amount,
        }