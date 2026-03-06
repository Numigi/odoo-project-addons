# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def create_analytic_lines(self):
        """
        Force the project_id on analytic lines based on the task's project
        when task is set on the move line.
        """
        result = super().create_analytic_lines()

        # Filter lines that have both task and project set
        lines_with_task = self.filtered(lambda l: l.task_id)

        for line in lines_with_task:
            # Check if task has a project defined to avoid resetting to False
            if line.task_id.project_id:
                # Update related analytic lines with the project from the task
                line.analytic_line_ids.write({
                    "project_id": line.task_id.project_id.id
                })

        return result
