# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, _


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    def _get_wip_timesheet_line_description(self):
        task = _("(task: {})").format(self.task_id.id)
        return "{} {}".format(self.name, task) if self.name else task

    def _get_wip_account(self):
        return self.project_id.project_type_id.wip_account_id
