# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.task_type = cls.env['project.task.type'].create({'name': 'New'})
        cls.task = cls.env['project.task'].create({
            'name': 'ttask',
        })
        cls.message = cls.env['mail.message'].xmlid_to_res_id(
            'project_task_stage_discussion_template.msg_discus1'
        )
        cls.message.res_id = cls.task.id

        cls.partner = cls.env['res.partner'].create({
            'name': 'tpartner',
        })
        partner_demo = cls.env.ref('base.partner_demo')
        cls.task.message_partner_ids = [(6, 0, [cls.partner.id, partner_demo.id])]

    def test_givenExternalMailIsUnchecked_thenInternalNoteSent(self):
        self.task_type.external_mail = False
        assert False

    def test_givenExternalMailIsChecked_thenMessageSent(self):
        self.task_type.external_mail = True
        assert False
