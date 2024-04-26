# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        if "milestone_id" in vals and vals.get("milestone_id"):
            milestone_id = self.env["project.milestone"].browse(vals["milestone_id"])
            if milestone_id.target_date:
                vals["date_deadline"] = milestone_id.target_date
        return super(ProjectTask, self).create(vals)

    def write(self, vals):
        if "milestone_id" in vals and vals.get("milestone_id"):
            milestone_id = self.env["project.milestone"].browse(vals["milestone_id"])
            if milestone_id.target_date:
                vals["date_deadline"] = milestone_id.target_date
        return super(ProjectTask, self).write(vals)

    @api.onchange("project_id", "milestone_id")
    def _onchange_project_propagate_deadline(self):
        if self.milestone_id and self.milestone_id.target_date:
            self.date_deadline = self.milestone_id.target_date
        else:
            super(ProjectTask, self)._onchange_project_propagate_deadline()
