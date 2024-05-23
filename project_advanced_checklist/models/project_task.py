# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Task(models.Model):

    _inherit = ["project.task"]

    checklist_id = fields.Many2one("project.checklist", string="Checklist")
    checklist_item_ids = fields.One2many(
        "project.task.checklist.item",
        "task_id",
        string="Items",
        copy=True,
    )
    checklist_progress = fields.Float(
        string="Checklist Progress", compute="_compute_checklist_progress"
    )

    @api.depends("checklist_item_ids")
    def _compute_checklist_progress(self):
        for record in self:
            sum_done = sum(1 for i in record.checklist_item_ids if i.result)
            total_items = len(record.checklist_item_ids)
            progress = (sum_done / total_items) * 100 if total_items else 0
            record.checklist_progress = progress or 0.01

    @api.onchange("checklist_id")
    def _onchange_checklist(self):
        self.checklist_item_ids = [
            (5, 0),
            *(
                (0, 0, self._make_checklist_item_vals(i))
                for i in self.checklist_id.item_ids
            ),
        ]

    def _make_checklist_item_vals(self, item):
        return {
            "sequence": item.sequence,
            "name": item.name,
            "description": item.description,
        }
