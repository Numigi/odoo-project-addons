# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import datetime

from odoo import api, models


class ProjectMilestoneTimeReport(models.AbstractModel):
    _inherit = "project.milestone.time.report"

    @api.model
    def _get_project_line(self, project):
        res = super()._get_project_line(project)
        res["date_start"] = project.date_start
        res["date_end"] = project.date
        res["total_remaining_hours"] = project.total_remaining_hours
        res["stage"] = project.stage_id
        return res

    @api.model
    def get_rendering_variables(self, project):
        res = super().get_rendering_variables(project)
        res["stage_lines"] = self._get_project_stages(project)
        return res

    @api.model
    def _get_project_stages(self, project):
        lots = project.child_ids.filtered(lambda p: not p.lump_sum)
        projects = project | lots
        stage_ids = list(set([p.stage_id.id for p in projects]))
        stage_ids = (
            self.env["project.stage"].browse(stage_ids).sorted(key=lambda p: p.sequence)
        )
        return [self._get_project_stage_line(s) for s in stage_ids]

    @api.model
    def _get_project_stage_line(self, stage):
        return {
            "stage": stage,
        }

    @api.model
    def _get_lines(self, project):
        super()._get_lines(project)
        lots = project.child_ids.filtered(lambda p: not p.lump_sum)
        projects = (project | lots).sorted(
            key=lambda a: (a.stage_id, (a.date_start or datetime.date(1970, 1, 1)))
        )
        return [self._get_project_line(p) for p in projects]
