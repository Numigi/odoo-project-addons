# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from uuid import uuid4
from odoo.exceptions import AccessError


class Task(models.Model):
    _inherit = "project.task"

    customer_reference = fields.Char()
