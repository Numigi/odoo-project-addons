# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class ProjectProject(models.Model):
    _inherit = "project.project"

    allow_edit_end_date = fields.Boolean("Allow edit end date")
    stage_name = fields.Char(related="stage_id.name")
    project_end_history_ids = fields.Many2many(
        "project.end.history",
        compute="_compute_project_end_history",
        string="Historics associated to this project",
    )
    project_end_history_count = fields.Integer(
        string="Historics",
        compute="_compute_project_end_history",
        groups="project.group_project_user",
    )

    def _compute_project_end_history(self):
        for project in self:
            project.project_end_history_ids = self.env["project.end.history"].search(
                [
                    ("project_id", "=", project.id),
                ]
            )
            project.project_end_history_count = len(project.project_end_history_ids)

    @api.multi
    def write(self, values):
        # Actually state is many2one (or related with it)
        # no external ID
        if "date" in values and self and self.stage_name == "Prévu":
            raise UserError(
                _(
                    "You can not modify the end date when project status is not 'Planned'."
                )
            )
        return super(ProjectProject, self).write(values)

    @api.multi
    def action_edit_end_date(self):
        self.ensure_one()
        action = self.env.ref("project_track_end_date.wizard_edit_end_date").read()[0]
        action["context"] = {
            "default_initial_date": self.date,
            "default_date": self.date,
            "default_project_id": self.id,
            "default_user_id": self.env.user.id,
            "default_company_id": self.env.user.company_id.id,
        }
        return action
