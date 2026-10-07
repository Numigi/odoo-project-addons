# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
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
    manager_approver_id = fields.Many2one(
        comodel_name="res.users",
        string="Manager Approver",
        readonly=True,
        copy=False,
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
    internal_notes = fields.Text(
        string="Notes",
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

    @api.constrains("date_start", "date_end", "project_id", "supervisor_id")
    def _check_period_and_overlap(self):
        for worksheet in self:
            worksheet._validate_date_chronology()
            worksheet._validate_same_week()
            worksheet._validate_no_overlap()

    def _validate_date_chronology(self):
        if self._is_date_range_invalid():
            self._raise_date_range_error()

    def _is_date_range_invalid(self):
        if not self.date_start or not self.date_end:
            return False
        return self.date_start > self.date_end

    def _raise_date_range_error(self):
        raise ValidationError(_("Period Start cannot be strictly greater than Period End."))

    def _validate_same_week(self):
        if self._has_both_dates() and not self._is_same_week():
            self._raise_same_week_error()

    def _has_both_dates(self):
        # Ensure both dates are set before performing calendar calculations
        return bool(self.date_start and self.date_end)

    def _is_same_week(self):
        # Extract ISO year and ISO week number to compare calendar weeks
        start_iso = self.date_start.isocalendar()
        end_iso = self.date_end.isocalendar()
        return start_iso[0] == end_iso[0] and start_iso[1] == end_iso[1]

    def _raise_same_week_error(self):
        raise ValidationError(
            _("The period start and end dates must fall within the same "
              "calendar week (Monday to Sunday).")
        )

    def _validate_no_overlap(self):
        if self._has_overlapping_worksheet():
            self._raise_overlap_error()

    def _has_overlapping_worksheet(self):
        # Query the database to find any overlapping worksheet for the same context
        domain = self._get_overlap_domain()
        return bool(self.search_count(domain))

    def _get_overlap_domain(self):
        return [
            ("id", "!=", self.id),
            ("project_id", "=", self.project_id.id),
            ("supervisor_id", "=", self.supervisor_id.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]

    def _raise_overlap_error(self):
        raise ValidationError(
            _("You cannot have overlapping worksheets for the same project and supervisor.")
        )

    def action_reset_to_draft(self):
        """ Allow supervisor to reset the worksheet to waiting approval state. """
        self.ensure_one()
        self._check_reset_rights()
        self._process_timesheets_for_reset()
        self._invalidate_access_token()
        self.write({"state": "new"})

    def _check_reset_rights(self):
        # Before client approval (new/open/pending), the supervisor may still
        # reset the worksheet to correct the hours, even once transmitted.
        # Once approved (confirmed), the action is reserved to a manager.
        if self._is_worksheet_confirmed():
            self._check_user_is_manager()
        else:
            self._check_supervisor_or_manager_rights()

    def _is_worksheet_confirmed(self):
        return self.state == "confirmed"

    def _check_user_is_manager(self):
        if not self._is_user_manager():
            self._raise_manager_access_error()

    def _is_user_manager(self):
        return self.env.user.has_group("project_worksheet.group_project_worksheet_manager")

    def _raise_supervisor_access_error(self):
        raise UserError(
            _("Only the assigned supervisor or a manager can perform this action.")
        )

    def _raise_manager_access_error(self):
        raise UserError(
            _("Only a worksheet manager can reset a confirmed worksheet to draft.")
        )

    def _process_timesheets_for_reset(self):
        if self.timesheet_ids:
            self._check_and_unlink_timesheets()

    def _check_and_unlink_timesheets(self):
        self._validate_no_locked_timesheets()
        self._unlink_timesheets()

    def _validate_no_locked_timesheets(self):
        if self._has_locked_timesheets():
            self._raise_locked_timesheet_error()

    def _has_locked_timesheets(self):
        locked_timesheets = (t for t in self.timesheet_ids if self._is_timesheet_locked(t))
        return any(locked_timesheets)

    def _is_timesheet_locked(self, timesheet):
        # A timesheet is locked if its sheet (hr_timesheet_sheet) has progressed
        # past draft. That module is optional, so when it is not installed the
        # sheet_id field is absent and no timesheet can be locked.
        return timesheet.sheet_id.state in ("confirm", "done")

    def _raise_locked_timesheet_error(self):
        raise UserError(
            _("Some timesheets are already locked. "
              "A timesheet administrator must unlock them first.")
        )

    def _unlink_timesheets(self):
        # Bypass timesheet deletion restrictions during worksheet reset
        self.timesheet_ids.with_context(bypass_worksheet_lock=True).unlink()

    def _invalidate_access_token(self):
        # Clear token so previously sent client links become invalid
        self.access_token = False

    def action_open(self):
        self.ensure_one()
        self._check_supervisor_or_manager_rights()
        self._validate_approval_conditions()
        self._generate_timesheets_if_empty()
        self.write({"state": "open"})

    def _check_supervisor_or_manager_rights(self):
        # Ensure the action is only performed by the assigned supervisor or a manager
        if not self._is_user_manager() and not self._is_current_user_supervisor():
            self._raise_supervisor_access_error()

    def _is_current_user_supervisor(self):
        return self.env.user == self.supervisor_id.user_id

    def _validate_approval_conditions(self):
        for worksheet in self:
            worksheet._check_has_lines_and_hours()

    def _check_has_lines_and_hours(self):
        if not self.line_ids or self.total_hours <= 0.0:
            self._raise_empty_worksheet_error()

    def _raise_empty_worksheet_error(self):
        raise UserError(_("You cannot approve a worksheet with no lines or zero total hours."))

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
        self.manager_approver_id = self.env.user
        self._confirm_worksheet("manager")
        message = _("Worksheet approved internally by manager: %s") % self.env.user.name
        self.message_post(body=message)

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

    def _generate_timesheets_if_empty(self):
        if not self.timesheet_ids:
            self._generate_timesheets()

    def _send_approval_email(self):
        template_id = self.env.ref("project_worksheet.email_template_worksheet_approval").id
        self.message_post_with_template(
            template_id,
            composition_mode="comment",
            message_type="comment",
        )

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
        self._send_confirmation_email()

    def _send_confirmation_email(self):
        template_id = self._get_confirmation_template_id()
        for worksheet in self:
            worksheet._post_confirmation_message(template_id)

    def _get_confirmation_template_id(self):
        return self.env.ref("project_worksheet.email_template_worksheet_confirmed").id

    def _post_confirmation_message(self, template_id):
        # Post the message using the appropriate user context
        record = self._get_mail_sender_record()
        record.message_post_with_template(
            template_id,
            composition_mode="comment",
            message_type="comment",
        )

    def _get_mail_sender_record(self):
        # Use root user (OdooBot) if the client is the one confirming the worksheet
        if self.approval_source == "client":
            return self._get_root_user_record()
        return self

    def _get_root_user_record(self):
        root_user = self.env.ref("base.user_root")
        return self.with_user(root_user)

    def _generate_timesheets(self):
        timesheet_model = self.env["account.analytic.line"].sudo().with_context(
            bypass_worksheet_lock=True
        )
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
            "name": line.name or "/",
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

    def unlink(self):
        self._check_unlink_allowed()
        return super().unlink()

    def _check_unlink_allowed(self):
        for worksheet in self:
            worksheet._validate_state_for_unlink()

    def _validate_state_for_unlink(self):
        if not self.state == "new":
            raise UserError(
                _("You can only delete a worksheet in the 'New' state")
            )
