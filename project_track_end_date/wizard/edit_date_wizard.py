# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EditDateWizard(models.TransientModel):
    _name = "edit.date.wizard"
    _description = "Edit Date Wizard"

    initial_date = fields.Date(string="Initial date")
    date = fields.Date(string="Date")
    company_id = fields.Many2one("res.company", string="Company")
    user_id = fields.Many2one("res.users", string="Author")
    reason = fields.Text("Access warning")
    project_id = fields.Many2one("project.project", string="Project")

    @api.multi
    def action_update_date(self):
        self.ensure_one()
        self.project_id.date = self.date

        data = {
            "update_on": self.create_date,
            "initial_date": self.initial_date,
            "date": self.date,
            "week_interval_date": (self.date - self.initial_date).days / 7,
            "total_week_duration": (self.date - self.project_id.date_start).days / 7,
            "company_id": self.company_id.id,
            "user_id": self.user_id.id,
            "reason": self.reason,
            "project_id": self.project_id.id,
        }

        self.env["project.end.history"].sudo().create(data)
        return {"type": "ir.actions.act_window_close"}
