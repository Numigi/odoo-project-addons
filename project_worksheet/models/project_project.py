# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    worksheet_count = fields.Integer(
        string="Worksheet Count",
        compute="_compute_worksheet_count",
    )

    def _compute_worksheet_count(self):
        # Compute the number of worksheets linked to each project
        worksheet_model = self.env["project.worksheet"]
        for project in self:
            project.worksheet_count = worksheet_model.search_count(
                [("project_id", "=", project.id)]
            )

    def action_view_worksheets(self):
        self.ensure_one()
        # Return the action to open the worksheets tree view
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "project_worksheet.project_worksheet_action"
        )
        action["domain"] = [("project_id", "=", self.id)]
        action["context"] = {"default_project_id": self.id}
        return action