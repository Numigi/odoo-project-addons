# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_demo = cls.env.ref('base.user_demo')
        cls.discussion_type = cls.env.ref('mail.mt_comment')
        cls.internal_note_type = cls.env.ref('mail.mt_note')
        cls.template = cls.env.ref(
            'project_task_stage_external_mail.demo_mail_template_task_open')
        cls.project = cls.env['project.project'].create({
            'name': 'Project 1',
        })
        cls.external_partner = cls.env['res.partner'].create({
            'name': 'tpartner',
            'email': 'tpartner@example.com',
        })
        cls.project.message_subscribe([cls.external_partner.id])

        cls.stage1 = cls.env['project.task.type'].create({
            'name': 'New',
            'mail_template_id': cls.template.id,
            'external_mail': False,
            'project_ids': [(4, cls.project.id)],
        })
        cls.stage2 = cls.env['project.task.type'].create({
            'name': 'Open',
            'mail_template_id': cls.template.id,
            'external_mail': True,
            'project_ids': [(4, cls.project.id)],
        })

        cls.task1 = cls.env['project.task'].create({
            'name': 'ttask 1',
            'stage_id': cls.stage1.id,
            'partner_id': cls.user_demo.partner_id.id,
            'project_id': cls.project.id,
            'allowed_user_ids': [(4, cls.user_demo.id)],

        })
        cls.task2 = cls.env['project.task'].create({
            'name': 'ttask 2',
            'stage_id': cls.stage2.id,
            'partner_id': cls.user_demo.partner_id.id,
            'project_id': cls.project.id,
            'allowed_user_ids': [(4, cls.user_demo.id)],

        })

    def _get_sent_message(self, task):
        messages = task.message_ids.filtered(
            lambda m: 'Task Open: ' in (m.subject or '')).sorted(
                key=lambda s: s.id, reverse=True)
        return messages

    def _get_message_recipients(self, task):
        message = self._get_sent_message(task)
        return message.mapped('notification_ids.res_partner_id')

    def test_givenExternalMailIsUnChecked_thenInternalNote(self):
        assert self._get_sent_message(self.task1).subtype_id == self.internal_note_type

    def test_givenExternalMailIsUnchecked_thenExternalPartnerNotInRecipients(self):
        assert self._get_message_recipients(self.task1)
        assert self.external_partner not in self._get_message_recipients(self.task1)

    def test_givenExternalMailIsChecked_thenCommentSent(self):
        assert self._get_sent_message(self.task2).subtype_id == self.discussion_type

    def test_givenExternalMailIsChecked_thenExternalPartnerInRecipients(self):
        assert self.external_partner in self._get_message_recipients(self.task2)
