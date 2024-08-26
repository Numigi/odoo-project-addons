# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License: AGPL-3.0 or later. See http://www.gnu.org/licenses/agpl

from odoo import models


class ProjectMeetingMinutes(models.Model):
    _inherit = "meeting.minutes.project"

    def _get_records_from_domain(self, domain, kpi):
        if self.project_id and self.project_id.parent_id:
            domain += [("project_id", "child_of", self.project_id.parent_id.id or False)]
            return self.env[kpi.model].search(domain) if domain else False
        else:
            return super(ProjectMeetingMinutes, self)._get_records_from_domain(domain, kpi)
