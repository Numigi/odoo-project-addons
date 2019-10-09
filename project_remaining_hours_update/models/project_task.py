# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _


class Task(models.Model):

    _inherit = 'project.task'

    remaining_hours_ids = fields.One2many(
        'project.task.remaining.hours',
        'task_id',
        'Remaining Hours History',
    )

    @api.depends(
        'effective_hours', 'subtask_effective_hours', 'planned_hours',
        'remaining_hours_ids.remaining_hours_change'
    )
    def _compute_remaining_hours(self):
        super()._compute_remaining_hours()
        for task in self:
            remaining_hours_change = sum(task.mapped('remaining_hours_ids.remaining_hours_change'))
            task.remaining_hours += remaining_hours_change

    def update_remaining_hours(self, new_remaining_hours, user, comment):
        """Update the remaining hours on the given task.

        :param new_remaining_hours: the new remaining hours
        :param user: the user who the task
        """
        self.check_access_rights('write')
        self.check_access_rule('write')
        self.env['project.task.remaining.hours'].sudo().create_from_task(
            self, new_remaining_hours, user, comment=comment,
        )

    @api.model
    def create(self, vals):
        """After creating the task, log the current remaining hours of the task.

        The remaining hours line created is indempotent.
        It is only created for logging/reporting purpose.
        """
        task = super().create(vals)
        task.update_remaining_hours(
            task.remaining_hours, self.env.user, comment=_('Task created')
        )
        return task

    @api.multi
    def write(self, vals):
        """After updating the planned hours, log the current remaining hours of the task.

        The remaining hours line created is indempotent.

        However, the new value for planned hours has impact over the computation
        of remaining hours. This must be reflected on the history of remaining hours.
        """
        res = super().write(vals)

        if 'planned_hours' in vals:
            for task in self:
                task.update_remaining_hours(
                    task.remaining_hours, self.env.user, comment=_('Planned hours updated')
                )

        return res
