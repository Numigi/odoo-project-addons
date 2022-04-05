# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Project(models.Model):

    _inherit = "project.project"

    @api.multi
    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        default, milestones_no_copy = self._milestones_no_copy(default)
        project = super().copy(default)
        if not milestones_no_copy:
            project._link_tasks_to_milestones()
        return project

    def _milestones_no_copy(self, default):
        context = dict(self.env.context or {})
        milestones_no_copy = "milestones_no_copy" in context and context["milestones_no_copy"]
        if milestones_no_copy:
            default["milestone_ids"] = False
        return default, milestones_no_copy

    def _link_tasks_to_milestones(self):
        for task in self.with_context(active_test=False).task_ids.filtered("milestone_id"):
            task.milestone_id = self._find_equivalent_milestone(task.milestone_id)

    def _find_equivalent_milestone(self, milestone):
        return next(
            (
                m
                for m in self.with_context(active_test=False).milestone_ids
                if m.name == milestone.name
            ),
            None,
        )

    @api.multi
    def write(self, vals):
        res = super(Project, self).write(vals)
        self._de_active_milestones(vals)
        return res

    def _de_active_milestones(self, vals):
        if {"active", "use_milestones"} & set(vals):
            self._set_active_milestones(vals)

    def _set_active_milestones(self, vals):
        for project in self:
            active = project._get_active_milestones(vals)
            project.with_context(active_test=False).milestone_ids.filtered(
                lambda milestone: milestone.active_toggle
            ).write({"active": active})

    def _get_active_milestones(self, vals):
        if "use_milestones" in vals:
            use_milestones = vals["use_milestones"]
        else:
            use_milestones = self.use_milestones
        if "active" in vals:
            active = vals["active"]
        else:
            active = self.active
        return use_milestones and active
