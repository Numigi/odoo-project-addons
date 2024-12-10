# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rate = fields.Float(string="Achievement Rate", required=True)
    mail_template_id = fields.Many2one(
        "mail.template", string="Template", required=True
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        if not self.rate or not self.mail_template_id:
            raise ValidationError("The Achievement rate must be greater than 0")
        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_mail_template',
            self.mail_template_id.id,
        )
        self.env['ir.config_parameter'].set_param(
            'project_milestone_progress_notification.default_rate', self.rate
        )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            mail_template_id=int(
                self.env['ir.config_parameter'].get_param(
                    'project_milestone_progress_notification.default_mail_template'
                )
                or 0
            ),
            rate=float(
                self.env['ir.config_parameter'].get_param(
                    'project_milestone_progress_notification.default_rate'
                )
                or 0.0
            ),
        )
        return res
