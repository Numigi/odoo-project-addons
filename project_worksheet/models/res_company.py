# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    worksheet_approval_delay = fields.Integer(
        string="Worksheet Approval Delay (Days)",
        default=7,
        help="Number of days before a manager can force approval.",
    )