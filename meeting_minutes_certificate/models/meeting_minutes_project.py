# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from base64 import b64encode
from odoo import fields, models, api, _
from odoo.exceptions import AccessError


class MeetingMinutesProject(models.Model):
    _inherit = "meeting.minutes.project"
    _order = "task_id desc"

    signature_ids = fields.One2many(
        "meeting.minutes.signature",
        "minutes_id",
    )

    certificate_report_id = fields.Many2one(
        "ir.actions.report",
        domain=[
            ("report_type", "=", "aeroo"),
            ("model", "=", "meeting.minutes.project"),
        ],
    )

    access_url = fields.Char(compute="_compute_access_url")

    signed_by_all = fields.Boolean(compute="_compute_signed_by_all")

    certificate_enabled = fields.Boolean(string="Training Certificate")
    certificate_file = fields.Binary(attachment=True, readonly=True)
    certificate_filename = fields.Char(readonly=True)

    @property
    def trainer_signature_ids(self):
        return self.signature_ids.filtered(lambda s: s.type_ == "trainer")

    @property
    def participant_signature_ids(self):
        return self.signature_ids.filtered(lambda s: s.type_ == "participant")

    def _compute_access_url(self):
        for minutes in self:
            minutes.access_url = "/my/training-certificate/%s" % minutes.task_id.id

    @api.depends("signature_ids.state")
    def _compute_signed_by_all(self):
        for minutes in self:
            signatures = minutes.signature_ids
            minutes.signed_by_all = signatures and all(
                s.state == "done" for s in signatures
            )

    @api.multi
    def write(self, vals):
        super().write(vals)

        if "signature_ids" in vals:
            for minutes in self:
                minutes._auto_subscribe_trainer()

        return True

    def preview_on_portal(self):
        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": self.access_url,
        }

    def print_certificate(self):
        return self.certificate_report_id.report_action(self)

    def send_certificate(self):
        self._render_certificate_file()

        for line in self.signature_ids:
            line.send_certificate()

    def request_signatures(self):
        unsent_lines = self.mapped("signature_ids").filtered(
            lambda l: l.state == "draft"
        )
        for line in unsent_lines:
            line.request_signature()

    def is_signed_by(self, user):
        line = self._get_signature_line(user)
        return line.state == "done"

    def _is_user_authorized(self, user, token):
        line = self._get_signature_line(user, token)
        if line:
            return True

        try:
            self.sudo(user).check_access_rights("read")
            self.sudo(user).check_access_rule("read")
        except AccessError:
            return False

        return True

    def _get_signature_line(self, user, token=None):
        partner = user.partner_id
        return self.signature_ids.filtered(
            lambda s: (token and s.access_token == token) or s.partner_id == partner
        )[:1]

    def _auto_subscribe_trainer(self):
        partners = self.trainer_signature_ids.mapped("partner_id")
        if partners:
            self._message_subscribe(partners.ids)

    def _get_default_trainer(self):
        return self.task_id.user_id.partner_id

    @api.onchange("certificate_enabled")
    def _onchange_certificate_enabled(self):
        if self.certificate_enabled:
            self._set_default_trainer_signature()

        self._update_signature_lines()

    @api.onchange("partner_ids")
    def _onchange_partner_ids(self):
        self._update_signature_lines()

    def _set_default_trainer_signature(self):
        trainer = self._get_default_trainer()
        if trainer:
            self.signature_ids |= self.env["meeting.minutes.signature"].new(
                {
                    "partner_id": trainer.id,
                    "type_": "trainer",
                }
            )

    def _update_signature_lines(self):
        if self.certificate_enabled:
            self.signature_ids -= self._get_unrequired_signature_lines()
            self.signature_ids |= self._get_missing_signature_lines()
        else:
            self.signature_ids = False

    def _get_missing_signature_lines(self):
        signatures = self.env["meeting.minutes.signature"]

        for partner in self._get_missing_participants():
            signatures |= self._new_participant_line(partner)

        return signatures

    def _get_unrequired_signature_lines(self):
        return self.signature_ids.filtered(
            lambda l: l.partner_id not in self.partner_ids and l.state == "draft"
        )

    def _get_missing_participants(self):
        participants = self.partner_ids - self._get_default_trainer()
        recorded_participants = self.mapped("signature_ids.partner_id")
        return participants - recorded_participants

    def _new_participant_line(self, partner):
        return self.env["meeting.minutes.signature"].new(
            {
                "partner_id": partner,
                "type_": "participant",
            }
        )

    def _notify_signed_by(self, partner):
        self.message_post(
            body=_("{} signed the training certificate.").format(partner.display_name),
            message_type="comment",
            subtype="mt_comment",
        )

    def _notify_signed_by_all(self):
        self.message_post(
            body=_("All participants signed the training certificate."),
            message_type="comment",
            subtype="mt_comment",
        )

    def _render_certificate_file(self):
        report = self.certificate_report_id

        filename = report.get_aeroo_filename(self, "pdf")
        data, _ = report.render_aeroo([self.id], force_output_format="pdf")

        self.certificate_file = b64encode(data)
        self.certificate_filename = filename
