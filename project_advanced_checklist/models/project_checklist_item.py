# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ChecklistItem(models.Model):
    _name = "project.checklist.item"
    _order = "sequence"
    _description = "Project Checklist Item"

    checklist_id = fields.Many2one(
        "project.checklist", ondelete="cascade", required=True
    )

    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
