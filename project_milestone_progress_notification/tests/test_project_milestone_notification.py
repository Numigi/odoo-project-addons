# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.project_milestone.tests.test_project_milestone import (
    TestProjectMilestone,
)


class TestProjectMilestoneNotification(TestProjectMilestone):
    def setUp(self):
        super().setUp()
        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_notify_manager', True
        )
        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', 60.0
        )
        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_mail_template',
            self.env.ref(
                'project_milestone_progress_notification.mail_template_project_milestone_progress_notification'
            ).id,
        )

    def test_project_milestone_notification(self):
        milestone1 = self.test_project_milestone_1

        self.assertEqual(milestone1.progress, 50)

        # Create another task to increase the progress
        task = self.env['project.task'].create(
            {
                'name': 'TestTask',
                'project_id': self.test_project.id,
                'milestone_id': self.test_project_milestone_1.id,
                'stage_id': self.test_close_stage.id,
            }
        )

        # Milestone progress should be 66.66666666666666
        self.assertAlmostEqual(milestone1.progress, 66.66, places=1)
        # Check if the mail is sent linked to the milestone.abs
        # Check in mail.mail table, model: project.milestone, res_id: milestone1.id
        mail = self._get_mail(milestone1)
        # Count sent mail should be 1
        self.assertEqual(len(mail), 1)
        self.assertEqual(milestone1.notification_sent, True)

        # If all the tasks are closed, the milestone progress should be 100 and the mail should not be sent
        self._make_all_tasks_closed(milestone1)

        self.assertEqual(milestone1.progress, 100)

        mail = self._get_mail(milestone1)
        # Count sent mail should be always 1
        self.assertEqual(len(mail), 1)

        # If all the tasks are set to open
        for task in milestone1.project_task_ids:
            task.stage_id = self.test_open_stage
        self.assertEqual(milestone1.progress, 0)
        self.assertEqual(milestone1.notification_sent, False)

        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', 33.0
        )

        task.stage_id = self.test_close_stage

        # Milestone progress should be 33.33333333333333
        self.assertAlmostEqual(milestone1.progress, 33.33, places=1)
        mail = self._get_mail(milestone1)
        # Count sent mail should be 2 now
        self.assertEqual(len(mail), 2)
        self.assertEqual(milestone1.notification_sent, True)

        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', 90.0
        )

        self._make_all_tasks_closed(milestone1)

        # Milestone progress should be 100
        self.assertEqual(milestone1.progress, 100)
        mail = self._get_mail(milestone1)
        # Count sent mail should be 3 now
        self.assertEqual(len(mail), 3)
        self.assertEqual(milestone1.notification_sent, True)

    def _make_all_tasks_closed(self, milestone):
        for task in milestone.project_task_ids:
            task.stage_id = self.test_close_stage

    def _get_mail(self, milestone):
        return self.env['mail.mail'].search(
            [
                ('model', '=', 'project.milestone'),
                ('res_id', '=', milestone.id),
            ]
        )
