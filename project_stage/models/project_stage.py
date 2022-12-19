# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectStage(models.Model):
    _name = 'project.stage'
    _description = 'Project Stage'
    _order = 'sequence'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer()
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    fold = fields.Boolean(
        string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.'
    )


class ProjectWithStage(models.Model):
    _inherit = 'project.project'

    def compute_default_stage(self):
        return self.env['project.stage'].search([('fold', '=', False)], order='sequence', limit=1).id

    stage_id = fields.Many2one(
        'project.stage', 'Stage', ondelete='restrict', index=True, default=compute_default_stage,
        tracking=True)
