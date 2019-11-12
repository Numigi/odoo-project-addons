# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTaskWithParentProject(models.Model):
    """Add parent_project_id to tasks.

    This field is used to navigate to the tasks from a parent project.
    """

    _inherit = 'project.task'

    parent_project_id = fields.Many2one(
        'project.project', 'Parent Project',
        compute='_compute_parent_project_id', store=True, index=True)

    @api.depends('project_id', 'project_id.is_parent', 'project_id.parent_id')
    def _compute_parent_project_id(self):
        """Compute the parent projects of a task."""
        for task in self:
            task.parent_project_id = (
                task.project_id if task.project_id.is_parent else
                task.project_id.parent_id
            )
