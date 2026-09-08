# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectWorksheetComplement(models.TransientModel):
    _name = "project.worksheet.complement"
    _description = "Create Complementary Worksheet"

    worksheet_id = fields.Many2one(
        comodel_name="project.worksheet",
        string="Original Worksheet",
        required=True,
        default=lambda self: self.env.context.get("active_id"),
    )

    def action_create_complement(self):
        self.ensure_one()
        new_worksheet = self._create_new_worksheet()
        return self._get_action_view_worksheet(new_worksheet)

    def _create_new_worksheet(self):
        worksheet_model = self.env["project.worksheet"]
        return worksheet_model.create(self._prepare_worksheet_vals())

    def _prepare_worksheet_vals(self):
        return {
            "project_id": self.worksheet_id.project_id.id,
            "company_id": self.worksheet_id.company_id.id,
            "supervisor_id": self.worksheet_id.supervisor_id.id,
            "date_start": self.worksheet_id.date_start,
            "date_end": self.worksheet_id.date_end,
            "partner_approver_id": self.worksheet_id.partner_approver_id.id,
            "state": "new",
        }

    def _get_action_view_worksheet(self, worksheet):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "project_worksheet.project_worksheet_action"
        )
        action["views"] = [(False, "form")]
        action["res_id"] = worksheet.id
        return action
