# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License: AGPL-3.0 or later. See http://www.gnu.org/licenses/agpl

from odoo import models


class ProjectMeetingMinutes(models.Model):
    _inherit = "meeting.minutes.project"

    def _get_records_from_domain(self, domain, kpi):
        if self.project_id and self.project_id.parent_id:
            if kpi.model in ['project.task', 'project.project']:
                field = "project_id" if kpi.model == 'project.task' else "id"
                domain += [(field, "child_of", self.project_id.parent_id.id or False)]
            return self.env[kpi.model].search(domain) if domain else False
        else:
            return super(ProjectMeetingMinutes, self)._get_records_from_domain(
                domain, kpi
            )

    def _get_steering_kpis(self, model_list):
        model_list = [model_list]
        model_list.append("project.project")
        return super(ProjectMeetingMinutes, self)._get_steering_kpis(model_list)

    def _prepare_project_steering_line_values(self, rec):
        if rec._name == "project.project":
            return {
                "meeting_minutes_id": self.id,
                "project_id": rec.id,
                "name": rec.display_name,
                "task_id": False,
            }
        else:
            return super(
                ProjectMeetingMinutes, self
            )._prepare_project_steering_line_values(rec)
