# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class Project(models.Model):

    _inherit = "project.project"

    active_toggle = fields.Boolean(string="Toggle active", default=True)

    def toggle_active(self):
        res = super(Project, self).toggle_active()
        self.toggle_active_change()
        return res

    def toggle_active_change(self):

        for project in self:
            project.active_toggle = project.active

    def write(self, vals):
        res = super(Project, self).write(vals)

        if "active" in vals and vals["active"]:
            self._project_not_active()

        return res

    def _project_not_active(self):
        self.filtered(lambda project: not project.active_toggle).write({"active": False})
