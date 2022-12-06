# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProjectAssignment(models.Model):
    _inherit = 'project.assignment'

    def _check_project_manager(self, project):
        if not project.is_manager:
            raise ValidationError(
                _('You are not allowed to create / modify an assignment'
                  ' for a project on which you are not assigned an '
                  '"Is a manager" role.'))

    @api.model
    def create(self, vals):
        if 'project_id' in vals:
            project = self.env['project.project'].browse(
                vals['project_id'])
            self._check_project_manager(project)
        return super(ProjectAssignment, self).create(vals)

    @api.multi
    def write(self, vals):
        project = self.env['project.project']
        for rec in self:
            if 'project_id' in vals:
                project = self.env['project.project'].browse(
                        vals['project_id'])
            elif rec.project_id:
                project = rec.project_id
            if project:
                self._check_project_manager(project)
        return super(ProjectAssignment, self).write(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.project_id:
                self._check_project_manager(rec.project_id)
        return super(ProjectAssignment, self).unlink()
