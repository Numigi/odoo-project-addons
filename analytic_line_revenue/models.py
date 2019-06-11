# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    revenue = fields.Boolean(track_visibility='onchange')
