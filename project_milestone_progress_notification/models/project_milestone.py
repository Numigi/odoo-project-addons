# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'

    notification_sent = fields.Boolean(string="Notification Sent")
    last_rate = fields.Float(string="Last Rate")
    progress_check = fields.Boolean(
        string="Last Progress Rate",
        store=True,
        compute='_compute_progress_check',
    )

    @api.depends('progress')
    def _compute_progress_check(self):
        rate = float(
            self.env['ir.config_parameter']
            .sudo()
            .get_param('project_milestone_progress_notification.default_rate')
        )
        for milestone in self:
            should_send_notification = milestone.progress >= rate and (
                not milestone.notification_sent or milestone.last_rate < rate
            )
            if should_send_notification:
                template_id = (
                    self.env['ir.config_parameter']
                    .sudo()
                    .get_param(
                        'project_milestone_progress_notification.default_mail_template'
                    )
                )
                milestone.message_post_with_template(int(template_id))
                milestone.write({'notification_sent': True, 'last_rate': rate})
            elif milestone.progress < rate and milestone.notification_sent:
                milestone.write({'notification_sent': False, 'last_rate': rate})
            else:
                pass

            self.env.cr.commit()
            milestone.progress_check = True
