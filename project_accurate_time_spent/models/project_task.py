# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class Task(models.Model):

    _inherit = "project.task"

    @api.depends(
        'stage_id', 'timesheet_ids.unit_amount', 'planned_hours',
        'child_ids.planned_hours', 'child_ids.effective_hours', 'child_ids.children_hours',
        'child_ids.timesheet_ids.unit_amount')
    def _hours_get(self):
        """Compute the Sub-task Hours using the sum of time spent on sub-tasks.

        This method was taken from odoo/addons/hr_timesheet/models/project.py and adapted.
        Only the field children_hours is changed.

        The behavior of other fields based on children_hours are thus affected in cascade.
        """
        for task in self.sorted(key='id', reverse=True):
            children_hours = 0
            for child_task in task.child_ids:
                # Only the following line was modified from the original Odoo code
                children_hours += child_task.effective_hours + child_task.children_hours

            task.children_hours = children_hours
            task.effective_hours = sum(task.sudo().timesheet_ids.mapped('unit_amount'))
            task.remaining_hours = task.planned_hours - task.effective_hours - task.children_hours
            task.total_hours = max(task.planned_hours, task.effective_hours)
            task.total_hours_spent = task.effective_hours + task.children_hours
            task.delay_hours = max(-task.remaining_hours, 0.0)

            if task.stage_id and task.stage_id.fold:
                task.progress = 100.0
            elif task.planned_hours > 0.0:
                progress_ratio = task.effective_hours + task.children_hours / task.planned_hours
                task.progress = round(100.0 * progress_ratio, 2)
            else:
                task.progress = 0.0
