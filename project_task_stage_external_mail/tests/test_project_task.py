# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.discussion_type = cls.env.ref('mail.mt_comment')
        cls.internal_note_type = cls.env.ref('mail.mt_note')
        cls.template = cls.env.ref('project_task_stage_external_mail.demo_mail_template_task_open')
        cls.stage = cls.env['project.task.type'].create({
            'name': 'New',
            'mail_template_id': cls.template.id,
            'external_mail': True,
        })
        cls.task = cls.env['project.task'].create({
            'name': 'ttask',
            'stage_id':  cls.stage.id,

        })
        cls.external_partner = cls.env['res.partner'].create({
            'name': 'tpartner',
            'email': 'tpartner@example.com',

        })

        cls.task.message_subscribe([cls.external_partner.id])


    def _get_sent_message(self):
        return self.task.message_ids.filtered(lambda m: 'Task Open: ' in (m.subject or ''))

    def _get_message_recipients(self):
        message = self._get_sent_message()
        return message.mapped('notification_ids.res_partner_id')

    def test_givenExternalMailIsUnchecked_thenInternalNoteSent(self):
        self.stage.external_mail = False
        assert self._get_sent_message().subtype_id == self.discussion_type

    def test_givenExternalMailIsUnchecked_thenPartnerNotInRecipients(self):
        self.stage.external_mail = False
        assert self.external_partner not in self._get_message_recipients()

    def test_givenExternalMailIsChecked_thenMessageSent(self):
        assert self._get_sent_message().subtype_id == self.discussion_type

    # TODO: Port this test method
    # def test_givenExternalMailIsChecked_thenPartnerInRecipients(self):
    #     assert self.external_partner in self._get_message_recipients()
