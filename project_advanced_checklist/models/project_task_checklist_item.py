# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TaskChecklistItem(models.Model):
    _name = "project.task.checklist.item"
    _order = "sequence"
    _description = "Project Task Checklist Item"

    task_id = fields.Many2one("project.task", ondelete="restrict", required=True)
    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    result = fields.Selection(
        [("complete", "Complete"), ("cancel", "Cancel")],
        string="Result",
        readonly=True,
    )

    def click_done(self):
        self.result = "complete"

    def click_cancel(self):
        self.result = "cancel"
