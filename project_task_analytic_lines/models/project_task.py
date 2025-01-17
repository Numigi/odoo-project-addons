# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError


class Task(models.Model):
    """Prevent moving the task when used on journal entries.

    When the task is used on a journal entry, the task must not be
    moved to another project.

    A constraint is also checked on open invoices.
    This allows to return a more precise error message to the user.
    """

    _inherit = "project.task"

    def write(self, vals):
        if "project_id" in vals:
            tasks_with_changed_project = self.filtered(
                lambda t: t.project_id.id != vals["project_id"]
            )

            for task in tasks_with_changed_project:
                task._check_no_related_open_invoice()

        return super().write(vals)

    def _check_no_related_open_invoice(self):
        move_lines = (
            self.env["account.move.line"]
            .sudo()
            .search([("task_id", "in", self.ids), ("move_id.state", "=", "posted")])
        )
        if move_lines:
            task = move_lines[0].task_id
            move = move_lines[0].move_id
            raise ValidationError(
                _(
                    "The task {task} can not be moved to another project "
                    "because it is already bound to a posted journal entry ({move})."
                ).format(task=task.display_name, move=move.display_name)
            )
