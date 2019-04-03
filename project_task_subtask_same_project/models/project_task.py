# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


class ProjectTaskSubtaskSameProject(models.Model):

    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        """ Propagate the value of the project to the subtask when it is changed on the parent task."""
        for task in self:
            if task.child_ids and 'project_id' in vals:
                task.child_ids.write({'project_id': vals['project_id']})
        return super().write(vals)
