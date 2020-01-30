# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectWithParent(models.Model):
    """Add parent_id to projects."""

    _inherit = 'project.project'

    parent_id = fields.Many2one(
        'project.project', 'Parent Project', ondelete='restrict', index=True)
    child_ids = fields.One2many('project.project', 'parent_id', 'Iterations')
    children_count = fields.Integer(
        'Iteration Count', compute='_compute_children_count',
        compute_sudo=True,
    )
    is_parent = fields.Boolean(
        'Is Parent', compute='_compute_is_parent', store=True,
        compute_sudo=True,
    )

    @api.multi
    def name_get(self):
        """Add the parent project before the name of the iteration.

        Check the access rights for the projects to read.
        Then, bypass access checks to prevent errors related to the parent project.
        """
        self.check_access_rights('read')
        self.check_access_rule('read')
        self = self.sudo()

        iterations = self.filtered(lambda p: p.parent_id)
        other_projects = self.filtered(lambda p: not p.parent_id)
        res = super(ProjectWithParent, other_projects).name_get()
        res.extend(
            (p.id, ', '.join([p.parent_id.name, p.name]))
            for p in iterations
        )
        return res

    @api.depends('child_ids')
    def _compute_children_count(self):
        for project in self:
            project.children_count = len(project.child_ids)

    @api.depends('child_ids')
    def _compute_is_parent(self):
        for project in self:
            project.is_parent = bool(project.child_ids)

    @api.constrains('parent_id')
    def _check_parent_project_has_no_parent(self):
        projects_with_grand_parent = self.filtered(lambda p: p.parent_id.parent_id)

        for project in projects_with_grand_parent:
            raise ValidationError(
                _('The project {project_2} can not be the parent of {project_1} '
                  'because {project_2} is a child of {project_3}.')
                .format(
                    project_1=project.display_name,
                    project_2=project.parent_id.display_name,
                    project_3=project.parent_id.parent_id.display_name,
                ))

    @api.constrains('parent_id', 'child_ids')
    def _check_child_project_has_no_child(self):
        child_projects_with_children = self.filtered(lambda p: p.parent_id and p.child_ids)

        for project in child_projects_with_children:
            raise ValidationError(
                _('The project {project_1} can not be the child of {project_2} '
                  'because {project_2} is a child of {project_3}.')
                .format(
                    project_1=project.child_ids[0].display_name,
                    project_2=project.display_name,
                    project_3=project.parent_id.display_name,
                ))

    @api.constrains('parent_id')
    def _check_parent_id_is_not_its_own_parent(self):
        for project in self:
            if project.parent_id == project:
                raise ValidationError(
                    _('The project {project} can not be its own parent.')
                    .format(project=project))

    @api.onchange('parent_id')
    def _onchange_parent_set_default_partner(self):
        if self.parent_id:
            self.partner_id = self.parent_id.partner_id


class ProjectWithIterationInTaskCount(models.Model):
    """Add the iteration tasks to the number of tasks of a parent project."""

    _inherit = 'project.project'

    def _compute_task_count(self):
        super()._compute_task_count()
        for project in self:
            project.task_count += sum(project.mapped('child_ids.task_count'))
