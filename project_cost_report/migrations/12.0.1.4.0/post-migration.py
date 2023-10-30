# © 2021 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    categories = env['project.cost.category'].search([])
    for categ in categories:
        if categ.target_hourly_rate:
            categ.target_type = "hourly_rate"
