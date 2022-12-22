# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ProjectTaskWithDeadlineFromProject(models.Model):
    """Propagate the field date_deadline from projects to tasks."""

    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        task = super().create(vals)
        should_propagate_deadline = task.project_id and 'date_deadline' not in vals
        if should_propagate_deadline:
            task.date_deadline = task.project_id.date
        return task

    @api.multi
    def write(self, vals):
        should_propagate_deadline = vals.get('project_id') and 'date_deadline' not in vals
        if should_propagate_deadline:
            project = self.env['project.project'].browse(vals['project_id'])
            vals['date_deadline'] = project.date
        return super().write(vals)

    @api.onchange('project_id')
    def _onchange_project_propagate_deadline(self):
        self.date_deadline = self.project_id.date
