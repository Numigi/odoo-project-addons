# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
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

    def _set_project_steering_ids(self, kpi, records):
        # Add the section from KPI name
        self.project_steering_ids = [
            (0, 0, {"name": kpi.name, "display_type": "line_section"}),
        ]
        for rec in records:
            self.project_steering_ids = [
                (
                    0,
                    0,
                    {
                        "meeting_minutes_id": self.id,
                        "project_id": self.project_id.id,
                        "name": self.project_id.display_name,
                        "task_id": rec.id,
                    },
                ),
            ]
        return True

    def _get_records_from_domain(self, domain, kpi):
        if self.project_id:
            domain += [("project_id", "=", self.project_id.id or False)]
        return self.env[kpi.model].search(domain) if domain else False

    @api.model
    def _get_domain_context(self):
        return {
            "context_today": datetime.now,
            "relativedelta": relativedelta,
        }

    def _get_filter_domain(self, kpi):
        domain = []
        if kpi.primary_filter_domain:
            domain += safe_eval(kpi.primary_filter_domain)
        if kpi.date_filter_domain:
            domain += safe_eval(
                kpi.date_filter_domain, self._get_domain_context()
            )
        return domain

    def action_load_steering_data(self):
        self.ensure_one()
        steering_kpis = self.env["project.steering.kpi"].search([
            ("model", "=", "project.task")
        ], order="sequence")
        # Reset one2many field before loading data
        self.project_steering_ids = [
            (2, line.id, False) for line in self.project_steering_ids
        ]
        for kpi in steering_kpis:
            domain = self._get_filter_domain(kpi)
            records = self._get_records_from_domain(domain, kpi)
            if records:
                self._set_project_steering_ids(kpi, records)
        return True
