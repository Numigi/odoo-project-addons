# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, fields


class ProjectTaskTypeExternalMail(models.Model):
    _inherit = 'project.task.type'

    external_mail = fields.Boolean()


class ProjectTaskDiscussion(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _track_template(self, tracking):
        """ set the publication channel to discussion."""
        res = super()._track_template(tracking)
        task = self[0]
        task_type = task.stage_id
        if task_type.external_mail:
            res['stage_id'][-1]['subtype_id'] = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
        return res
