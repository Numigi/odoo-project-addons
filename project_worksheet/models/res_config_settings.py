# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    worksheet_approval_delay = fields.Integer(
        related="company_id.worksheet_approval_delay",
        readonly=False,
    )