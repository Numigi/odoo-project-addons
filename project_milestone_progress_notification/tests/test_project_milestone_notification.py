from odoo.tests import common


class TestMilestoneProgressNotification(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.test_project = self.env["project.project"].create({"name": "NumiProject"})
        self.test_project_milestone_1 = self.env["project.milestone"].create(
            {"name": "TestMilestone_1", "project_id": self.test_project.id}
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "project_milestone_progress_notification.default_rate", "75.0"
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "project_milestone_progress_notification.default_mail_template",
            self.env.ref(
                "project_milestone_progress_notification.mail_template_project_milestone_progress_notification"
            ).id,
        )

    def test_notification_sent_on_progress_reach(self):
        """
        Test if notification is sent when milestone progress reaches 75%
        with configuration rate set to 75%.
        """
        milestone = self.env["project.milestone"].create(
            {"name": "TestMilestone_1", "project_id": self.test_project.id}
        )
        milestone.progress = 74.9  # Progress below 75%
        self.assertFalse(milestone.notification_sent)

        milestone.progress = 75.0  # Progress reaches 75%
        milestone._check_and_send_progress_notification()
        self.assertTrue(milestone.notification_sent)

        # Check if a mail.message is created
        self.assertTrue(len(milestone.message_ids) > 0)
        self.assertEqual(
            milestone.message_ids[0].subtype_id, self.env.ref("mail.mt_comment")
        )

    def test_notification_not_sent_below_threshold(self):
        """
        Test if notification is not sent when milestone progress is below 75%
        with configuration rate set to 75%.
        """
        milestone = self.env["project.milestone"].create(
            {"name": "TestMilestone_1", "project_id": self.test_project.id}
        )
        milestone.progress = 74.9  # Progress below 75%
        nbr_messages = len(milestone.message_ids)
        milestone._check_and_send_progress_notification()
        self.assertFalse(milestone.notification_sent)
        # No new message should be created
        self.assertEqual(
            len(milestone.message_ids),
            nbr_messages,
            msg="No new message should be created",
        )

    def test_notification_not_resent_above_threshold(self):
        """
        Test if notification is not resent when progress is already above 75%
        and notification_sent is True.
        """
        milestone = self.env["project.milestone"].create(
            {
                "name": "TestMilestone_1",
                "project_id": self.test_project.id,
                "notification_sent": True,
            }
        )
        milestone.progress = 75.1  # Progress above 75%
        nbr_messages = len(milestone.message_ids)
        milestone._check_and_send_progress_notification()
        self.assertTrue(milestone.notification_sent)
        self.assertEqual(
            len(milestone.message_ids),
            nbr_messages,
            msg="No new message should be created",
        )

    def test_notification_resent_after_drop_and_rise(self):
        """
        Test if notification is resent when progress drops below 75%,
        then rises above 75% again.
        """
        milestone = self.env["project.milestone"].create(
            {
                "name": "TestMilestone_1",
                "project_id": self.test_project.id,
                "notification_sent": True,
            }
        )
        milestone.progress = 70.0  # Progress drops below 75%
        milestone._check_and_send_progress_notification()
        self.assertFalse(milestone.notification_sent)

        milestone.progress = 75.1  # Progress rises above 75%
        nbr_messages = len(milestone.message_ids)
        milestone._check_and_send_progress_notification()
        self.assertTrue(milestone.notification_sent)
        self.assertTrue(
            len(milestone.message_ids) > nbr_messages,
            msg="New message should be created",
        )
