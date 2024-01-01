# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from contextlib import contextmanager
from datetime import datetime
from uuid import uuid4
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MeetingMinutesSignature(models.Model):
    _name = "meeting.minutes.signature"
    _description = "Training Certificate Signature"
    _inherit = ["mail.thread"]
    _rec_name = "partner_id"

    minutes_id = fields.Many2one(
        "meeting.minutes.project",
        required=True,
        index=True,
        ondelete="cascade",
    )

    partner_id = fields.Many2one("res.partner", required=True)
    task_id = fields.Many2one("project.task", related="minutes_id.task_id")

    type_ = fields.Selection(
        [
            ("trainer", "Trainer"),
            ("participant", "Participant"),
        ],
        default="participant",
        required=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("done", "Done"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )

    signature_datetime = fields.Datetime(readonly=True)
    signature = fields.Binary(attachment=True, copy=False, readonly=True)
    access_token = fields.Char(groups="base.group_system", copy=False)

    def get_access_url(self, suffix=None):
        url = self.minutes_id.access_url

        if suffix:
            url += suffix

        query_params = "?access_token={}".format(self._portal_ensure_token())
        return url + query_params

    @property
    def has_to_be_signed(self):
        return self.state != "done"

    @api.model
    def create(self, values):
        line = super().create(values)
        line._message_subscribe([line.partner_id.id])
        if line.signature:
            values = {"signature": line.signature}
            line._track_signature(values, "signature")
        return line

    @api.multi
    def write(self, values):
        self._track_signature(values, "signature")
        return super().write(values)

    @api.multi
    def unlink(self):
        for line in self:
            if line.state == "done":
                raise ValidationError(
                    _("You may not delete a signed signature request.")
                )
        return super().unlink()

    def request_signature(self):
        self._notify_signature_request()
        self.state = "sent"

    def send_certificate(self):
        template = self.env.ref("meeting_minutes_certificate.mail_template_signed")
        attachment = self._make_certificate_attachment()
        self._send_message(template, attachments=attachment)

    def sign(self, signature):
        self.signature = signature
        self.state = "done"
        self.signature_datetime = datetime.now()
        self.minutes_id._notify_signed_by(self.partner_id)

        if self.minutes_id.signed_by_all:
            self.minutes_id._notify_signed_by_all()
            self.minutes_id.send_certificate()

    def _make_certificate_attachment(self):
        data = self.minutes_id.certificate_file
        filename = self.minutes_id.certificate_filename

        vals = self._get_attachment_vals(filename, data)
        return self.env["ir.attachment"].create(vals)

    def _get_attachment_vals(self, filename, data):
        return {
            "name": filename,
            "datas": data,
            "datas_fname": filename,
            "res_model": "mail.compose.message",
            "res_id": 0,
            "type": "binary",
        }

    def _notify_signature_request(self):
        template = self.env.ref("meeting_minutes_certificate.mail_template_request")
        self._send_message(template)

    def _send_message(self, template, attachments=None):
        res_id = self.id
        res_model = self._name
        composition_mode = "comment"
        context = {
            "active_id": res_id,
            "active_ids": [res_id],
            "active_model": res_model,
            "default_composition_mode": composition_mode,
            "default_model": res_model,
            "default_res_id": res_id,
            "default_template_id": template.id,
            "lang": self.partner_id.lang,
        }
        composer = self.env["mail.compose.message"].with_context(**context).create({})
        composer.partner_ids = self.partner_id
        onchange_data = composer.onchange_template_id(
            template.id, composition_mode, res_model, res_id
        )
        composer.write(onchange_data["value"])
        composer.write(
            {"attachment_ids": [(6, 0, attachments.ids if attachments else [])]}
        )
        return composer.send_mail()

    def _portal_ensure_token(self):
        self = self.sudo()
        if not self.access_token:
            self.write({"access_token": str(uuid4())})
        return self.access_token
