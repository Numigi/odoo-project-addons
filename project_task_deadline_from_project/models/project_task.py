# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTaskWithDeadlineFromProject(models.Model):
    """Propagate the field date_deadline from projects to tasks."""

    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        should_propagate_deadline = vals.get('project_id') and 'date_deadline' not in vals
        if should_propagate_deadline:
            vals['date_deadline'] = self._get_deadline_from_project_id(vals['project_id'])
        return super().create(vals)

    @api.multi
    def write(self, vals):
        should_propagate_deadline = vals.get('project_id') and 'date_deadline' not in vals
        if should_propagate_deadline:
            vals['date_deadline'] = self._get_deadline_from_project_id(vals['project_id'])
        return super().write(vals)

    def _get_deadline_from_project_id(self, project_id):
        project = self.env['project.project'].browse(project_id)
        return project.date

    @api.onchange('project_id')
    def _onchange_project_propagate_deadline(self):
        self.date_deadline = self.project_id.date
