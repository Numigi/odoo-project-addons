# Copyright 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval
from dateutil.relativedelta import relativedelta


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

    def _get_steering_data(self):
        # Level to check is on task
        steering_kpis = self.env["project.steering.kpi"].search(
            [("model", "=", "project.task")], order="sequence"
        )
        # Reset one2many field before loading data
        self.project_steering_ids = [(5, 0)]

        for kpi in steering_kpis:
            domain = [("project_id", "=", self.project_id.id or False)]
            if kpi.primary_filter_domain:
                domain += safe_eval(kpi.primary_filter_domain)
            self._add_record_from_domain(domain, kpi)

    def _add_record_from_domain(self, domain, kpi):
        records = self.env[kpi.model].search(domain)
        if records:
            # Add the section from KPI name
            self.project_steering_ids = [
                (0, 0, {"name": kpi.name, "display_type": "line_section"}),
            ]

        # Filter with date_filter_domain if set and result of primary filter not empty
        if kpi.date_filter_domain_id and records:
            domain = kpi.date_filter_domain_id.domain
            normalized_domain = (
                domain.replace("\n", "")
                .replace(" ", "")
                .replace("context_today()", "fields.Date.context_today(self)")
            )
            # Execute all the python code in normalized_domain
            # and replace it by its result
            last_domain = safe_eval(
                normalized_domain,
                {
                    "fields": fields,
                    "relativedelta": relativedelta,
                    "self": self,
                    "context": self.env.context,
                },
            )
            records = records.search(last_domain)

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
