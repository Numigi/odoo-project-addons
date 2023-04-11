# © 2023 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    parent_project_id = fields.Many2one(
        'project.project', 'Parent Project',
        compute='_compute_parent_project_id', store=True, index=True,
        compute_sudo=True,
    )

    @api.depends('project_id', 'project_id.is_parent', 'project_id.parent_id')
    def _compute_parent_project_id(self):
        """Compute the parent project of a milestone.

        If the project has no parent,
        then the parent project is the project itself.
        """
        for record in self:
            record.parent_project_id = (
                record.project_id if record.project_id.is_parent else
                record.project_id.parent_id
            )
