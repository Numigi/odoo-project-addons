# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectWithChatter(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'mail.activity.mixin']

    date = fields.Date(track_visibility='onchange')
    date_start = fields.Date(track_visibility='onchange')
