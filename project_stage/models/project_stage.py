# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, SUPERUSER_ID


class ProjectStage(models.Model):
    _name = "project.stage"
    _description = "Project Stage"
    _order = "sequence"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer()
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    fold = fields.Boolean(
        string="Folded in Kanban",
        help="""This stage is folded in the kanban view when there are
        no records in that stage to display.""",
    )


class ProjectWithStage(models.Model):
    _inherit = "project.project"

    def compute_default_stage(self):
        return (
            self.env["project.stage"]
            .search([("fold", "=", False)], order="sequence", limit=1)
            .id
        )

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [("id", "in", stages.ids)]
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID
        )
        return stages.browse(stage_ids)

    stage_id = fields.Many2one(
        "project.stage",
        "Stage",
        ondelete="restrict",
        index=True,
        default=compute_default_stage,
        group_expand="_read_group_stage_ids",
        tracking=True,
    )
