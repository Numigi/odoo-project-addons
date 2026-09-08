# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ProjectWorksheetLine(models.Model):
    _name = "project.worksheet.line"
    _description = "Project Worksheet Line"

    worksheet_id = fields.Many2one(
        comodel_name="project.worksheet",
        string="Worksheet",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=True,
    )
    project_id = fields.Many2one(
        related="worksheet_id.project_id",
        store=True,
    )
    task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task",
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    unit_amount = fields.Float(
        string="Hours",
        required=True,
    )

    @api.constrains("task_id")
    def _check_task_is_not_parent(self):
        lines_with_tasks = (line for line in self if line.task_id)
        for line in lines_with_tasks:
            self._validate_child_task(line.task_id)

    def _validate_child_task(self, task):
        if task.child_ids:
            self._raise_parent_task_error()

    def _raise_parent_task_error(self):
        raise UserError(_("You cannot record timesheets on a parent task."))