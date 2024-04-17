# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    active = fields.Boolean(string="Active", default=True)
    active_toggle = fields.Boolean(string="Toggle active", default=True)

    def toggle_active(self):
        res = super(ProjectMilestone, self).toggle_active()
        self.toggle_active_change()
        return res

    def toggle_active_change(self):
        for milestone in self:
            milestone.active_toggle = milestone.active

    def write(self, vals):
        res = super(ProjectMilestone, self).write(vals)

        if "project_id" in vals:
            self._remove_task_milestones(vals["project_id"])

        if "active" in vals and vals["active"]:
            self._milestone_not_active()
        return res

    def _remove_task_milestones(self, project_id):
        self.with_context(active_test=False).mapped("project_task_ids").filtered(
            lambda milestone: not project_id or milestone.project_id.id != project_id
        ).write({"milestone_id": False})

    def _milestone_not_active(self):
        self.filtered(lambda milestone: not milestone.active_toggle).write(
            {"active": False}
        )
