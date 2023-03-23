# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, _


class TaskRemainingHoursUpdate(models.TransientModel):

    _name = 'project.task.remaining.hours.update'
    _description = 'Task Remaining Hours Update Wizard'

    task_id = fields.Many2one('project.task')
    new_remaining_hours = fields.Float()
    comment = fields.Text()

    def validate(self):
        previous_value = self.task_id.remaining_hours

        self.task_id.update_remaining_hours(
            self.new_remaining_hours,
            user=self.env.user,
            comment=self.comment,
        )

        message = _('Remaining hours updated from {previous} to {new}.').format(
            previous=previous_value,
            new=self.new_remaining_hours,
        )

        if self.comment:
            message += '<br><br>{}'.format(self.comment)

        self.task_id.message_post(body=message)
