# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TaskRemainingHours(models.Model):

    _name = "project.task.remaining.hours"
    _description = "Remaining Hours History on Tasks"
    _order = "id desc"

    project_id = fields.Many2one(
        "project.project", related="task_id.project_id", store=True
    )
    task_id = fields.Many2one(
        "project.task", required=True, index=True, ondelete="cascade"
    )
    user_id = fields.Many2one("res.users", readonly=True)
    planned_hours = fields.Float()
    total_hours_spent = fields.Float()
    remaining_hours = fields.Float()
    remaining_hours_change = fields.Float()
    comment = fields.Text()

    def _get_remaining_hours_vals(self, task, new_remaining_hours, user, comment):
        remaining_hours_change = new_remaining_hours - task.remaining_hours
        return {
            "task_id": task.id,
            "remaining_hours": new_remaining_hours,
            "remaining_hours_change": remaining_hours_change,
            "planned_hours": task.planned_hours,
            "total_hours_spent": task.total_hours_spent,
            "user_id": user.id,
            "comment": comment,
        }

    def create_from_task(self, task, new_remaining_hours, user, comment):
        """Create a remaining hours history line from a task.

        :param task: the task for which to update remaining hours
        :param user: the user who the task
        :param new_remaining_hours: the new remaining hours
        :param comment: the comment why the remaining hours was updated
        """
        vals = self._get_remaining_hours_vals(
            task, new_remaining_hours, user, comment=comment
        )
        return self.create(vals)
