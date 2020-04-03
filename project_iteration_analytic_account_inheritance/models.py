# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class ProjectParentInheritance(models.Model):
    _inherit = "project.project"

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.set_analytic_account_from_parent()
        return record

    @api.multi
    def write(self, vals):
        super().write(vals)
        for record in self:
            if vals.get("parent_id"):
                record.set_analytic_account_from_parent()
            elif vals.get("analytic_account_id"):
                record.set_analytic_to_children()
        return True

    def set_analytic_account_from_parent(self):
        if self.parent_id:
            self.analytic_account_id = self.parent_id.analytic_account_id

    def set_analytic_to_children(self):
        for child in self.child_ids:
            child.analytic_account_id = self.analytic_account_id
