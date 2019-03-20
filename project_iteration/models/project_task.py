# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTaskWithParentProject(models.Model):
    """Add parent_project_ids to tasks.

    This field is used to navigate to the tasks from a parent project.
    """

    _inherit = 'project.task'

    parent_project_ids = fields.Many2many(
        'project.project', 'project_task_parent_rel', 'task_id', 'project_id',
        string='Parent Project', compute='_compute_parent_project_ids', store=True)

    @api.depends('project_id', 'project_id.parent_id')
    def _compute_parent_project_ids(self):
        """Compute the parent projects of a task."""
        for task in self:
            task.parent_project_ids = task.project_id | task.project_id.parent_id
