# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError
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
        compute="_compute_partner_id",
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
        default=lambda self: self._default_supervisor_id(),
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
    date_sent = fields.Datetime(
        string="Date Sent",
        readonly=False,
        copy=False,
    )
    date_approve = fields.Datetime(
        string="Approval Date",
        readonly=True,
        copy=False,
    )
    partner_approver_id = fields.Many2one(
        comodel_name="res.partner",
        string="Client Approver",
        tracking=True,
    )
    approval_source = fields.Selection(
        selection=[
            ("client", "Client"),
            ("manager", "Manager"),
        ],
        string="Approval Source",
        readonly=True,
        copy=False,
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

    def _default_supervisor_id(self):
        return self.env["hr.employee"].search([("user_id", "=", self.env.uid)], limit=1)

    @api.depends("line_ids.unit_amount")
    def _compute_total_hours(self):
        for worksheet in self:
            worksheet.total_hours = sum(worksheet.line_ids.mapped("unit_amount"))

    @api.depends("project_id.partner_id")
    def _compute_partner_id(self):
        for worksheet in self:
            worksheet.partner_id = worksheet._get_parent_company()

    def _get_parent_company(self):
        if not self.project_id.partner_id:
            return False
        return self.project_id.partner_id.commercial_partner_id

    @api.constrains("date_start", "date_end")
    def _check_date_range(self):
        for worksheet in self:
            worksheet._validate_date_chronology()

    def action_open(self):
        self.ensure_one()
        self.write({"state": "open"})

    def action_send_to_client(self):
        self.ensure_one()
        self._portal_ensure_token()
        self._generate_timesheets_if_empty()
        self._send_approval_email()
        self.write({
            "state": "pending",
            "date_sent": fields.Datetime.now(),
        })

    def action_remind_client(self):
        self.ensure_one()
        self._portal_ensure_token()
        return self._get_remind_client_action()

    def action_manager_confirm(self):
        self.ensure_one()
        self._confirm_worksheet("manager")

    def action_client_confirm(self):
        self.ensure_one()
        self._confirm_worksheet("client")

    def _default_name(self):
        return self.env["ir.sequence"].next_by_code("project.worksheet") or _("New")

    def _compute_access_url(self):
        super()._compute_access_url()
        for worksheet in self:
            worksheet.access_url = "/my/worksheet/%s/%s" % (
                worksheet.id,
                worksheet.access_token,
            )

    def _validate_date_chronology(self):
        if self._is_date_range_invalid():
            self._raise_date_range_error()

    def _is_date_range_invalid(self):
        if not self.date_start or not self.date_end:
            return False
        return self.date_start > self.date_end

    def _raise_date_range_error(self):
        raise ValidationError(_("Period Start cannot be strictly greater than Period End."))

    def _generate_timesheets_if_empty(self):
        if not self.timesheet_ids:
            self._generate_timesheets()

    def _send_approval_email(self):
        template = self.env.ref("project_worksheet.email_template_worksheet_approval")
        template.send_mail(self.id, force_send=True)

    def _get_remind_client_action(self):
        template = self.env.ref("project_worksheet.email_template_worksheet_approval")
        return {
            "name": _("Remind Client"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(False, "form")],
            "view_id": False,
            "target": "new",
            "context": self._get_remind_client_context(template),
        }

    def _get_remind_client_context(self, template):
        return {
            "default_model": self._name,
            "default_res_id": self.id,
            "default_use_template": True,
            "default_template_id": template.id,
            "default_composition_mode": "comment",
            "force_email": True,
        }

    def _confirm_worksheet(self, source):
        self.write({
            "state": "confirmed",
            "date_approve": fields.Datetime.now(),
            "approval_source": source,
        })

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

    @api.model
    def _cron_remind_pending_worksheets(self):
        worksheets = self.search([("state", "=", "pending")])
        for worksheet in worksheets:
            worksheet._process_reminder_if_needed()

    def _process_reminder_if_needed(self):
        if self._is_reminder_needed():
            self._create_reminder_activity()

    def _is_reminder_needed(self):
        if not self.date_sent:
            return False
        delay = self.company_id.worksheet_reminder_delay
        limit_date = self.date_sent + timedelta(days=delay)
        return fields.Datetime.now() >= limit_date

    def _create_reminder_activity(self):
        if not self._has_reminder_activity():
            self._schedule_new_reminder()

    def _has_reminder_activity(self):
        domain = self._get_existing_activity_domain()
        return bool(self.env["mail.activity"].search_count(domain))

    def _get_existing_activity_domain(self):
        return [
            ("res_model", "=", self._name),
            ("res_id", "=", self.id),
            ("summary", "=", "Follow up on client approval"),
        ]

    def _schedule_new_reminder(self):
        user_id = self._get_reminder_user_id()
        self.activity_schedule(
            "mail.mail_activity_data_todo",
            summary=_("Follow up on client approval"),
            note=_("This worksheet has been pending for more than the allowed delay."),
            user_id=user_id,
        )

    def _get_reminder_user_id(self):
        if self.supervisor_id.user_id:
            return self.supervisor_id.user_id.id
        return self.create_uid.id
