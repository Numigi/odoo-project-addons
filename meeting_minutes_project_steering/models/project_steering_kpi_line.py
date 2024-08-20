# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectSteeringKpiLine(models.Model):
    _name = "project.steering.kpi.line"
    _description = "Project Steering KPI Line"

    meeting_minutes_id = fields.Many2one(
        "project.meeting.minutes", string="Project Meeting Minutes", index=True
    )
    name = fields.Text(string="Notes")
    display_type = fields.Selection(
        [("line_section", "Section"), ("line_note", "Note")],
        default=False,
        help="Technical field for UX purpose.",
    )
    project_id = fields.Many2one("project.project", string="Project")
    project_end_date = fields.Date(related="project_id.date", string="Project Deadline")
    task_id = fields.Many2one("project.task", string="Task")
    task_date_planned = fields.Date(
        related="task_id.date_planned", string="Planned date"
    )
    task_date_deadline = fields.Date(related="task_id.date_deadline", string="Deadline")
