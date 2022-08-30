# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, models, fields


class ProjectAssignment(models.Model):

    _inherit = "project.assignment"

    @api.multi
    def _get_conflicting_domain(self):
        self.ensure_one()
        return [
                   ('id', '!=', self.id),
                   ('role_id', '=', self.role_id.id),
                   ('user_id', '=', self.user_id.id),
               ] + (
                   [('company_id', 'in', [False, self.company_id.id])]
                   if self.company_id else []
               ) + (
                   [('project_id', 'in', [False, self.project_id.id])]
                   if self.project_id else []
               ) + (
                   [('milestone_id', 'in', [False, self.milestone_id.id])]
                   if self.milestone_id else []
               )
    milestone_id = fields.Many2one(
        "project.milestone",
        string="Milestone",
        index=True,
        copy=False
    )

    _sql_constraints = [
                        (
                           'project_milestone_role_user_uniq',
                           'UNIQUE (project_id, role_id, user_id, milestone_id)',
                           'User may be assigned per role and per milestone only once within a project!'
                        ),
                        (
                            'project_role_user_uniq',
                            'Check(1=1)',
                            'User may be assigned per role and per milestone only once within a project!'
                        )
                        ]

    @api.onchange('milestone_id')
    def onchange_milestone(self):
        if self.milestone_id:
            project_id = self.milestone_id.project_id
            if project_id:
                self.project_id = project_id.id
                return {'domain': {'project_id': [('id', '=', project_id.id)]}}
        else:
            project_ids = self.env['project.project'].search([])
            if project_ids:
                return {'domain': {'project_id': [('id', 'in', project_ids.ids)]}}

    @api.onchange('project_id')
    def onchange_project(self):
        if self.project_id:
            return {'domain': {'milestone_id': [('project_id', '=', self.project_id.id)]}}
        else:
            milestone_ids = self.env['project.milestone'].search([])
            if milestone_ids:
                return {'domain': {'milestone_id': [('id', 'in', milestone_ids.ids)]}}
