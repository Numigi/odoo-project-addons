# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    active = fields.Boolean(string="Active", default=True)
    active_toggle = fields.Boolean(string="Toggle active", default=True)

    @api.multi
    def toggle_active(self):
        res = super(ProjectMilestone, self).toggle_active()
        for milestone in self:
            milestone.active_toggle = milestone.active
        return res

    @api.multi
    def write(self, vals):
        res = super(ProjectMilestone, self).write(vals)
        if "project_id" in vals:
            self._remove_task_milestones(vals["project_id"])
        return res

    def _remove_task_milestones(self, project_id):
        for milestone in self:
            milestone.with_context(active_test=False).project_task_ids.filtered(
                lambda milestone: not project_id or milestone.project_id.id != project_id
            ).write({"milestone_id": False})
