# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License: AGPL-3.0 or later. See http://www.gnu.org/licenses/agpl

from odoo import models


class ProjectMeetingMinutes(models.Model):
    _inherit = "meeting.minutes.project"

    def _get_project_domain(self):
        # if project has a parent, get all subprojects
        if self.project_id.parent_id:
            return [("project_id", "child_of", self.project_id.parent_id.id)]
        else:
            return super(ProjectMeetingMinutes, self)._get_project_domain()
