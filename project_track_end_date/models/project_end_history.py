# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectEndHistory(models.Model):
    _name = "project.end.history"
    _description = "Project End History"

    update_on = fields.Datetime(string="Update on")
    initial_date = fields.Date(string="Initial Date")
    date = fields.Date(string="Date")
    week_interval_date = fields.Float(string="Number of Reporting Weeks")
    total_week_duration = fields.Float(string="Total Project Duration (Weeks)")
    company_id = fields.Many2one("res.company", string="Company")
    user_id = fields.Many2one("res.users", string="Author")
    reason = fields.Text("Reason")
    project_id = fields.Many2one("project.project", string="Project")
