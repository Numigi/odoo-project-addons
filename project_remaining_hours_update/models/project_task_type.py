# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProjectTaskType(models.Model):

    _inherit = 'project.task.type'

    set_remaining_hours_to_0 = fields.Boolean()
