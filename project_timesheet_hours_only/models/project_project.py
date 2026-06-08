# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectProject(models.Model):
    _inherit = "project.project"

    def _compute_total_timesheet_time(self):
        for project in self:
            project._compute_project_timesheet_time()

    def _compute_project_timesheet_time(self):
        project_timesheets = self.timesheet_ids.filtered(lambda t: t.task_id)
        total_time = self._calculate_timesheet_total(project_timesheets)
        self.total_timesheet_time = int(round(total_time))


    def _calculate_timesheet_total(self, timesheets):
        total = sum(t.unit_amount * t.product_uom_id.factor_inv for t in timesheets)
        return total * self.timesheet_encode_uom_id.factor
