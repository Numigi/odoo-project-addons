# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_end_history_ids = fields.One2many(
        "project.end.history",
        "project_id",
        string="Historics associated to this project",
    )
    project_end_history_count = fields.Integer(
        string="Historics",
        compute="_compute_project_end_history",
        groups="project.group_project_manager",
    )
    expected_week_duration = fields.Float(
        string="Expected week duration",
        compute="_compute_expected_week_duration",
    )

    def _compute_expected_week_duration(self):
        for project in self:
            project.expected_week_duration = (
                (project.date - project.date_start).days / 7
                if project.date and project.date_start
                else 0
            )

    def _compute_project_end_history(self):
        for project in self:
            project.project_end_history_count =\
                len(project.project_end_history_ids)

    @api.multi
    def action_edit_end_date(self):
        self.ensure_one()
        action = self.env.ref("project_track_end_date.wizard_edit_end_date"
                              ).read()[0]
        action["context"] = {
            "default_initial_date": self.date,
            "default_date": self.date,
            "default_project_id": self.id,
            "default_user_id": self.env.user.id,
            "default_company_id": self.company_id.id,
        }
        return action
