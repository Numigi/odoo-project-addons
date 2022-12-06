# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    is_manager = fields.Boolean(
        "Is Manager", compute="_is_manager"
    )

    manager_ids = fields.Many2many('res.users',
                                   string='Managers',
                                   index=True,
                                   compute="_compute_manager_ids",
                                   store=True)

    def _is_manager(self):
        user = self.env.user
        for rec in self:
            rec.is_manager = rec.assignment_ids.filtered(
                    lambda a: a.role_id.is_manager
                    and a.user_id == user) \
                         or user.has_group('project.group_project_manager')

    @api.depends('assignment_ids', 'assignment_ids.role_id',
                 'assignment_ids.user_id',
                 'assignment_ids.role_id.is_manager')
    def _compute_manager_ids(self):
        for rec in self:
            rec.manager_ids = rec.assignment_ids.filtered(
                    lambda a: a.role_id.is_manager).mapped('user_id')
