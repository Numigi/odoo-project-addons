# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.tools.safe_eval import safe_eval


class ProjectMeetingMinutes(models.Model):
    _inherit = "meeting.minutes.project"

    project_steering_enabled = fields.Boolean(string="Project Steering")
    project_steering_ids = fields.One2many(
        "project.steering.kpi.line",
        "meeting_minutes_id",
        string="Project Steering",
        ondelete="cascade",
    )

    def load_steering_data(self):
        self.ensure_one()
        self._get_steering_data()
        return True

    def _get_project_domain(self):
        return [("project_id", "=", self.project_id.id or False)]

    def _get_steering_data(self):
        # Level to check is on task
        steering_kpis = self.env["project.steering.kpi"].search(
            [("model", "=", "project.task")], order="sequence"
        )
        # Reset one2many field before loading data
        self.project_steering_ids = [(5, 0)]

        for kpi in steering_kpis:
            domain = self._get_project_domain()
            if kpi.filter_domain:
                domain += safe_eval(kpi.filter_domain)
            self._add_record_from_domain(domain, kpi)

    def _add_record_from_domain(self, domain, kpi):
        # Add the section from KPI name
        self.project_steering_ids = [
            (0, 0, {"name": kpi.name, "display_type": "line_section"}),
        ]
        records = self.env[kpi.model].search(domain)
        # Append data after section
        self._prepare_data_in_section(records)

    def _prepare_data_in_section(self, records):
        for rec in records:
            self.project_steering_ids = [
                (
                    0,
                    0,
                    {
                        "meeting_minutes_id": self.id,
                        "project_id": rec.project_id.id,
                        "task_id": rec.id,
                    },
                ),
            ]
