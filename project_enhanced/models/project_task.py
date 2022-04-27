# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectTask(models.Model):

    _inherit = "project.task"

    active_toggle = fields.Boolean(string="Toggle active", default=True)

    @api.multi
    def toggle_active(self):
        res = super(ProjectTask, self).toggle_active()
        self.toggle_active_change()
        return res

    @api.multi
    def toggle_active_change(self):

        for task in self:
            task.active_toggle = task.active

    @api.multi
    def write(self, vals):
        res = super(ProjectTask, self).write(vals)

        if "active" in vals and vals["active"]:
            self._task_not_active()

        return res

    def _task_not_active(self):
        self.filtered(lambda task: not task.active_toggle).write({"active": False})
