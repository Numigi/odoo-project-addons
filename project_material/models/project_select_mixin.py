# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectSelect(models.AbstractModel):
    """Project Select Mixin.

    This mixin adds a technical computed field to allow constrain
    the domain when selecting the task.

    This field is not stored and only used as a helper in the global list view of material.

    This mixin expects the concrete class to have a many2one field `task_id`.
    """

    _name = "project.select.mixin"
    _description = "Project Selection Mixin"

    project_select_id = fields.Many2one(
        "project.project",
        "Project Select",
        compute="_compute_project_select",
        inverse=lambda self: None,
    )

    def _compute_project_select(self):
        for record in self:
            record.project_select_id = record.project_id

    @api.onchange("project_select_id")
    def _onchange_project_select_reset_task(self):
        if self.project_select_id != self.task_id.project_id:
            self.task_id = False
