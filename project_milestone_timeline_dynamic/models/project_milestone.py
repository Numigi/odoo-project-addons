# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    @api.constrains("start_date")
    def _check_start_date_and_dependencies_end_date(self):
        for milestone in self:
            sorted_child_ids = milestone.child_ids.sorted(
                key="target_date", reverse=True
            )
            child_last_end_dates = milestone.child_ids.mapped("target_date")

            if (
                child_last_end_dates
                and milestone.start_date
                and milestone.start_date < max(child_last_end_dates)
            ):
                raise ValidationError(
                    _(
                        "The milestone %s - %s is dependent on this "
                        "milestone and has a %s end date."
                    )
                    % (
                        sorted_child_ids[0].name,
                        sorted_child_ids[0].project_id.name,
                        fields.Date.to_string(max(child_last_end_dates)),
                    )
                )

    @api.onchange("child_ids")
    def _onchange_child_ids(self):
        child_last_end_dates = self.child_ids.sorted(
            key="target_date", reverse=True
        ).mapped("target_date")

        self._assign_new_timeline(
            self.start_date, self.target_date, child_last_end_dates
        )

    def write(self, vals):
        for milestone in self:
            if "target_date" in vals:
                parent_milestone = milestone._get_parent_milestone()
                if parent_milestone:
                    parent_milestone.update_parent_timeline(milestone, vals)
        return super(ProjectMilestone, self).write(vals)

    def _assign_new_timeline(self, start_date, target_date, child_last_end_dates):
        if child_last_end_dates and (
            not start_date or start_date <= child_last_end_dates[0]
        ):
            milestone_duration = target_date - start_date
            self.start_date = child_last_end_dates[0] + timedelta(days=1)
            self.target_date = self.start_date + milestone_duration

    def _get_parent_milestone(self):
        self.env.cr.execute(
            "SELECT milestone_id FROM rel_project_milestone_dependencies "
            "WHERE child_id = %s",
            (self.id,),
        )
        milestone_id = self.env.cr.fetchone()
        return (
            self.env["project.milestone"].browse(milestone_id[0])
            if milestone_id
            else None
        )

    def update_parent_timeline(self, child_milestone, updated_val):
        child_ids = self.child_ids - child_milestone
        child_last_end_dates = child_ids.sorted(key="target_date", reverse=True).mapped(
            "target_date"
        )
        child_target_date = fields.Date.from_string(updated_val["target_date"])

        if child_target_date not in child_last_end_dates:
            child_last_end_dates.append(child_target_date)
            child_last_end_dates.sort(reverse=True)
            self._assign_new_timeline(
                self.start_date, self.target_date, child_last_end_dates
            )