# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    child_ids = fields.Many2many('project.milestone',
                                 'rel_project_milestone_dependencies',
                                 'milestone_id', 'child_id',
                                 string="Dependencies")

    @api.constrains('child_ids')
    def _check_recursion(self):
        if not self._check_m2m_recursion('child_ids'):
            raise ValidationError(_("You cannot create recursive "
                                    "dependencies between milestones."))
