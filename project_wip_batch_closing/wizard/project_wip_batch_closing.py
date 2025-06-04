# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectWipBatchClosing(models.TransientModel):
    """Wizard that allows to define a custom date to post the WIP transfer move."""

    _name = "project.wip.batch.closing"
    _description = "Project Transfer WIP To CGS Batch"

    state = fields.Selection(
        [("date_step", "Select Closing Date"),
         ("project_step", "Select Project"),
         ("processing_step", "Processing"), ], string="Status", readonly=True,
        required=True, default="date_step", )

    date_cutoff = fields.Date("Cut Off Date", required=True)


    def action_validate(self):
        return True

