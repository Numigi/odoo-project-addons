# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    meeting_minutes_ids = fields.One2many(
        "meeting.minutes.project",
        "project_id",
        string="Meeting minutes associated to this project",
    )
    meeting_minutes_count = fields.Integer(
        string="Meeting minutes",
        compute="_compute_nbr_meeting",
        groups="project.group_project_user",
    )
    pending_actions_ids = fields.Many2many(
        "mail.activity", string="Pending Actions",
        compute="_compute_pending_action_ids"
    )

    @api.multi
    def _compute_nbr_meeting(self):
        for project in self:
            project.meeting_minutes_count = len(
                project.meeting_minutes_ids
            )

    @api.multi
    def _compute_pending_action_ids(self):
        homework = self.env.ref("meeting_minutes_project.activity_homework")
        today = fields.Date.context_today(self)

        for rec in self:
            activities = self.env["mail.activity"].search(
                [("res_id", "in", rec.task_ids.ids)],
            )
            rec.pending_actions_ids = activities.filtered(
                lambda a: (
                    a.activity_type_id == homework
                    and a.res_model == "project.task"
                    and a.date_deadline < today
                )
            )
