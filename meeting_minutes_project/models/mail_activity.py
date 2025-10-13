# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.model
    def default_get(self, fields):
        res = super(MailActivity, self).default_get(fields)
        if res.get("res_model") == "project.task":
            res["task_id"] = self.env["project.task"].browse(res["res_id"]).id
        return res

    task_id = fields.Many2one("project.task", string="Task")
    meeting_minutes_id = fields.Many2one(
        "meeting.minutes.project", string="Meeting Minutes"
    )

    @api.onchange("task_id")
    def onchange_task_id(self):
        if self.task_id:
            self.res_id = self.task_id.id
            self.res_model = "project.task"
            self.res_model_id = self.env["ir.model"]._get("project.task").id
            self.activity_type_id = self.env.ref(
                "meeting_minutes_project.activity_homework"
            ).id
