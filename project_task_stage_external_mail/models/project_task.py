# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, fields


class ProjectTaskTypeExternalMail(models.Model):

    _inherit = 'project.task.type'

    external_mail = fields.Boolean()


class ProjectTask(models.Model):

    _inherit = 'project.task'



    def _track_template(self, changes):
        """Set the publication channel to discussion."""
        res = super()._track_template(changes)
        task = self[0]
        task_type = task.stage_id
        if 'stage_id' in res and task_type.external_mail:
            res['stage_id'][-1]['subtype_id'] = self.env.ref('mail.mt_comment').id
        return res


