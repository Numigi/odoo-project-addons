# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Checklist(models.Model):
    _name = "project.checklist"
    _order = "name"
    _description = "Project Checklist"

    name = fields.Char(string="Name", required=True)
    item_ids = fields.One2many("project.checklist.item", "checklist_id", string="Items")
    description = fields.Char(string="Description")
