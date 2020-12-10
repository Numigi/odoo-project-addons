# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Project(models.Model):

    _inherit = "project.project"

    outsourcing_po_count = fields.Integer(compute="_compute_outsourcing_po_count")

    def _compute_outsourcing_po_count(self):
        for project in self:
            project.outsourcing_po_count = self.env["purchase.order"].search(
                [("project_id", "=", project.id), ("state", "!=", "cancel")], count=True
            )
