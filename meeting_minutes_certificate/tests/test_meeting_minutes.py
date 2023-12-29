# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from base64 import b64encode
from datetime import timedelta
from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase
from odoo import api, fields, models, tools, _
from ..controllers.portal import (
    Portal,
    SIGN_PAGE_TEMPLATE,
    CERTIFICATE_LIST_PAGE_TEMPLATE,
)


class TestMeetingMinutes(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_portal = cls.env.ref("base.group_portal")
        cls.group_project = cls.env.ref("project.group_project_user")

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Participant 1",
                "email": "participant1@example.com",
            }
        )

        cls.user = cls.env["res.users"].create(
            {
                "partner_id": cls.partner.id,
                "groups_id": [(4, cls.group_portal.id)],
                "email": "participant@example.com",
                "login": "participant",
                "name": "Participant",
            }
        )

        cls.trainer = cls.env["res.users"].create(
            {
                "email": "trainer@example.com",
                "login": "trainer",
                "name": "Trainer",
                "groups_id": [(4, cls.group_project.id)],
            }
        )

        cls.public_user = cls.env.ref("base.public_user")

        cls.project = cls.env["project.project"].create({"name": "Project 1"})

        cls.task = cls.env["project.task"].create(
            {
                "project_id": cls.project.id,
                "name": "Task 1",
                "user_id": cls.trainer.id,
            }
        )

        cls.report = cls.env.ref("meeting_minutes_certificate.meeting_minutes_report")
        cls.minutes = cls.task.get_meeting_minutes()
        cls.minutes.certificate_enabled = True
        cls.minutes.certificate_report_id = cls.report
        cls.minutes._onchange_certificate_enabled()

        cls.signature_content = b"R0lGODlhAQABAAAAACwAAAAAAQABAAAC"
        cls.trainer_line = cls.minutes.trainer_signature_ids

    def test_portal_url(self):
        assert self.minutes.access_url == f"/my/training-certificate/{self.task.id}"

    def test_trainer_auto_subscribe(self):
        assert self.trainer.partner_id in self.minutes.message_partner_ids

    def test_trainer_auto_subscribe__on_trainer_change(self):
        trainer_2 = self.trainer.partner_id.copy()
        trainer_vals = {
            "partner_id": trainer_2.id,
            "type_": "trainer",
        }
        vals = {"signature_ids": [(0, 0, trainer_vals)]}
        self.minutes.write(vals)
        assert trainer_2 in self.minutes.message_partner_ids

    def test_signature__partner_auto_subscribe(self):
        assert self.trainer.partner_id in self.trainer_line.message_partner_ids

    def test_request_signatures(self):
        line = self._make_signature_line(self.partner)
        line.request_signature()
        message = self._get_latest_message(line)
        assert message
        assert self.partner in message.partner_ids
        assert line.state == "sent"

    def test_preview_on_portal(self):
        action = self.minutes.preview_on_portal()
        assert action["url"] == self.minutes.access_url

    def test_trainer(self):
        line = self.minutes.trainer_signature_ids
        assert line.partner_id == self.trainer.partner_id

    def test_participants__certificate_not_enabled(self):
        self.minutes.partner_ids = self.partner | self.trainer.partner_id
        self.minutes.certificate_enabled = False
        self.minutes._onchange_partner_ids()
        assert not self.minutes.signature_ids

    def test_participants(self):
        self.minutes.partner_ids = self.partner | self.trainer.partner_id
        self.minutes._onchange_partner_ids()
        line = self.minutes.participant_signature_ids
        assert line.partner_id == self.partner

    def test_participants__already_recorded(self):
        self.minutes.partner_ids = self.partner
        self.minutes._onchange_partner_ids()
        line = self.minutes.participant_signature_ids
        self.minutes._onchange_partner_ids()
        assert line.partner_id == self.partner
        assert line == self.minutes.participant_signature_ids

    def test_participants__changed(self):
        self.minutes.partner_ids = self.partner
        self.minutes._onchange_partner_ids()
        new_partner = self.partner.copy()
        self.minutes.partner_ids = new_partner
        self.minutes._onchange_partner_ids()
        line = self.minutes.participant_signature_ids
        assert line.partner_id == new_partner

    def test_participants__not_removed_if_already_sent(self):
        self.minutes.partner_ids = self.partner
        self.minutes._onchange_partner_ids()
        line = self.minutes.participant_signature_ids
        self.minutes.partner_ids = False
        self.minutes.participant_signature_ids.state = "sent"
        self.minutes._onchange_partner_ids()
        assert line == self.minutes.participant_signature_ids

    def test_participants_from_task(self):
        task = self.task.copy()
        task._message_subscribe(self.partner.ids)
        minutes = task.get_meeting_minutes()
        minutes.certificate_enabled = True
        minutes._onchange_certificate_enabled()
        assert minutes.participant_signature_ids.partner_id == self.partner

    def test_send_certificate(self):
        self.minutes.send_certificate()
        message = self._get_latest_message(self.trainer_line)
        assert "Here is the certificate" in message.body

    def test_request_signatures(self):
        self.minutes.sudo(self.trainer).request_signatures()
        assert self.trainer_line.state == "sent"

    def test_print_certificate(self):
        assert self.minutes.print_certificate()

    def test_sign(self):
        line = self._make_signature_line(self.partner)
        line.sign(self.signature_content)
        assert line.state == "done"
        assert not line.has_to_be_signed

    def test_is_signed_by(self):
        assert not self.minutes.is_signed_by(self.user)
        line = self._make_signature_line(self.partner)
        line.sign(self.signature_content)
        assert self.minutes.is_signed_by(self.user)

    def test_signed_by_one_partner(self):
        line = self._make_signature_line(self.partner)
        line.sign(self.signature_content)

        message = self._get_latest_message(self.minutes)
        assert f"{self.partner.name} signed" in message.body
        assert message.subtype_id == self.env.ref("mail.mt_comment")

    def test_signed_by_all_partners(self):
        line = self._make_signature_line(self.partner)
        line.sign(self.signature_content)
        self.trainer_line.sign(self.signature_content)

        message = self._get_latest_message(self.minutes)
        assert "All participants signed" in message.body
        assert message.subtype_id == self.env.ref("mail.mt_comment")

        message = self._get_latest_message(line)
        assert "Here is the certificate" in message.body

    def test_training_certificate_list(self):
        response = self._get_certificate_list_page_response()
        assert response.template == CERTIFICATE_LIST_PAGE_TEMPLATE

    def test_sign_page(self):
        self._make_signature_line(self.partner)
        response = self._get_sign_page_response()
        assert response.template == SIGN_PAGE_TEMPLATE

    def test_sign_page__not_allowed(self):
        partner = self.partner.copy()
        self._make_signature_line(partner)
        response = self._get_sign_page_response(user=self.user)
        assert response.template != SIGN_PAGE_TEMPLATE

    def test_sign_page__user_allowed(self):
        self._make_signature_line(self.partner)
        response = self._get_sign_page_response(user=self.user)
        assert response.template == SIGN_PAGE_TEMPLATE

    def test_sign_page__with_token(self):
        signature = self._make_signature_line(self.partner)
        token = signature._portal_ensure_token()
        response = self._get_sign_page_response(user=self.public_user, token=token)
        assert response.template == SIGN_PAGE_TEMPLATE

    def test_print_report(self):
        self._print_report()

    def test_sign_controller(self):
        line = self._make_signature_line(self.partner)
        self._sign_certificate(self.signature_content)
        assert line.state == "done"

    def test_delete_signature_done(self):
        self.trainer_line.state = "done"
        with pytest.raises(ValidationError):
            self.trainer_line.unlink()

    def _get_sign_page_response(self, user=None, token=None):
        env = self.env if user is None else self.env(user=user.id)
        with mock_odoo_request(env):
            return Portal().training_certificate_page(self.task.id, access_token=token)

    def _get_certificate_list_page_response(self, user=None):
        env = self.env if user is None else self.env(user=user.id)
        with mock_odoo_request(env):
            return Portal().training_certificate_list_page(self.task.id)

    def _print_report(self):
        with mock_odoo_request(self.env):
            return Portal().training_certificate_report(self.task.id)

    def _sign_certificate(self, signature_content):
        env = self.env(user=self.user.id)
        with mock_odoo_request(env, routing_type="json"):
            return Portal().training_certificate_sign(
                self.task.id,
                signature=signature_content,
            )

    def _make_signature_line(self, partner):
        return self.env["meeting.minutes.signature"].create(
            {
                "minutes_id": self.minutes.id,
                "partner_id": partner.id,
            }
        )

    def _get_latest_message(self, record):
        return record.message_ids[:1]
