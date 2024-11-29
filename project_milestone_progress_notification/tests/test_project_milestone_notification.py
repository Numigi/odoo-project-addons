# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests import common


class TestProjectMilestoneNotification(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProjectMilestoneNotification, cls).setUpClass()
        cls.test_project = cls.env['project.project'].create({'name': 'NumiProject'})
        cls.test_project_milestone_1 = cls.env['project.milestone'].create(
            {'name': 'TestMilestone_1', 'project_id': cls.test_project.id}
        )
        cls.test_task = cls.env['project.task'].create(
            {
                'name': 'TestNumigiTask1',
                'project_id': cls.test_project.id,
                'milestone_id': cls.test_project_milestone_1.id,
            }
        )
        cls.env['project.task'].create(
            {
                'name': 'TestNumigiTask2',
                'project_id': cls.test_project.id,
                'milestone_id': cls.test_project_milestone_1.id,
            }
        )
        cls.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_notify_manager', True
        )
        cls.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', 60.0
        )
        cls.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_mail_template',
            cls.env.ref(
                'project_milestone_progress_notification.mail_template_project_milestone_progress_notification'
            ).id,
        )

    def test_project_milestone_notification(self):
        # Test is directly linked to the milestone progress to avoid checking if
        # the progress is updated by the task or not. The calculation of the progress
        # may vary depending on modules installed. Like project_milestone_time_progress
        # module will update the progress based on the task hours, not the task stage.

        milestone1 = self.test_project_milestone_1

        # Milestone progress is initially 50
        milestone1.progress = 50

        # Milestone progress changed to 66.66
        milestone1.progress = 66.66
        # Check if the mail is sent linked to the milestone.abs
        # Check in mail.mail table, model: project.milestone, res_id: milestone1.id
        mail = self._get_mail(milestone1)
        # Count sent mail should be 1
        self.assertEqual(len(mail), 1)
        self.assertEqual(milestone1.notification_sent, True)

        # Milestone progress is now 100
        milestone1.progress = 100

        mail = self._get_mail(milestone1)
        # Count sent mail should be always 1
        self.assertEqual(len(mail), 1)

        milestone1.progress = 0
        milestone1.notification_sent = False

        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', 33.0
        )

        # Milestone progress is 33.33
        milestone1.progress = 33.33
        mail = self._get_mail(milestone1)
        # Count sent mail should be 2 now
        self.assertEqual(len(mail), 2)
        self.assertEqual(milestone1.notification_sent, True)

        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', 90.0
        )

        # Milestone progress is now 100
        milestone1.progress = 100
        mail = self._get_mail(milestone1)
        # Count sent mail should be 3 now
        self.assertEqual(len(mail), 3)
        self.assertEqual(milestone1.notification_sent, True)

    def _get_mail(self, milestone):
        return self.env['mail.mail'].search(
            [
                ('model', '=', 'project.milestone'),
                ('res_id', '=', milestone.id),
            ]
        )
