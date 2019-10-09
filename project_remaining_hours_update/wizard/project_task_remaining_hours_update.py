# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TaskRemainingHoursUpdate(models.TransientModel):

    _name = 'project.task.remaining.hours.update'
    _description = 'Task Remaining Hours Update Wizard'

    task_id = fields.Many2one('project.task')
    new_remaining_hours = fields.Float()
    comment = fields.Text()

    def validate(self):
        self.task_id.update_remaining_hours(
            self.new_remaining_hours,
            user=self.env.user,
            comment=self.comment,
        )
