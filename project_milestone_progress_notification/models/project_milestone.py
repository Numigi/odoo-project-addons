# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'

    notification_sent = fields.Boolean(
        string="Notification Sent",
        default=False,
    )

    # Methode called by the corn "Check and Send Milestone Progress Notification"
    def _check_and_send_progress_notification(self):
        config_param = self.env["ir.config_parameter"].sudo()
        rate = float(config_param.get_param(
            "project_milestone_progress_notification.default_rate"
        ))
        template_id = config_param.get_param(
            "project_milestone_progress_notification.default_mail_template"
        )
        milestones = self.search([])
        for milestone in milestones:
            if milestone.progress >= rate and not milestone.notification_sent:
                # Send notification if it hasn't been sent or rate was updated
                milestone.message_post_with_template(int(template_id))
                milestone.notification_sent = True
            elif milestone.progress < rate and milestone.notification_sent:
                # Reset notification if progress drops below the rate
                milestone.notification_sent = False
