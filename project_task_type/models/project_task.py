# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskWithType(models.Model):
    """Add the field task_type_id on tasks."""

    _inherit = 'project.task'

    task_type_id = fields.Many2one(
        'task.type', 'Type', ondelete='restrict', index=True,
        tracking=True)
