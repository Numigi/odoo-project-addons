# Copyright 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class ProjectMilestone(models.Model):
    _name = "project.milestone"

    _inherit = ["project.milestone", "mail.thread", "mail.activity.mixin"]

    active = fields.Boolean(string="Active", default=True)
    active_toggle = fields.Boolean(string="Toggle active", default=True)
    sequence = fields.Integer()
    progress = fields.Float(
        compute="_compute_milestone_progress",
        store=True,
        help="Percentage of Completed Tasks vs Incomplete Tasks.",
    )

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
        self.with_context(active_test=False).mapped("task_ids").filtered(
            lambda milestone: not project_id or milestone.project_id.id != project_id
        ).write({"milestone_id": False})

    def _milestone_not_active(self):
        self.filtered(lambda milestone: not milestone.active_toggle).write(
            {"active": False}
        )

    @api.depends("task_ids.stage_id")
    def _compute_milestone_progress(self):
        total_tasks_count = 0.0
        closed_tasks_count = 0.0
        for record in self:
            for task_record in record.task_ids:
                total_tasks_count += 1
                if task_record.stage_id.closed:
                    closed_tasks_count += 1
            if total_tasks_count > 0:
                record.progress = (closed_tasks_count / total_tasks_count) * 100
            else:
                record.progress = 0.0
